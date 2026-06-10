import json
from pathlib import Path
from datetime import datetime

from google import genai

from app.config import GEMINI_API_KEY, DATA_DIR, GENERATION_MODEL
from app.rag.retriever import retrieve_relevant_chunks

client = genai.Client(api_key=GEMINI_API_KEY)


GENERATED_WORKOUTS_DIR = DATA_DIR / "generated_workouts"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def save_json(path: Path, data) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def create_run_dir() -> Path:
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    run_dir = GENERATED_WORKOUTS_DIR / timestamp
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def append_workout_to_history(
    history_path: Path,
    workout_history: list,
    workout_plan: str,
    checkin: dict,
    retrieved_chunks: list,
    status: str = "completed",
) -> None:
    new_entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "source": "generated_rag_plan",
        "status": status,
        "checkin": checkin,
        "generated_plan": workout_plan,
        "rag_sources": [
            {
                "source": chunk["source"],
                "score": round(chunk["score"], 4),
            }
            for chunk in retrieved_chunks
        ],
    }

    workout_history.append(new_entry)

    history_path.write_text(
        json.dumps(workout_history, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

def build_retrieval_query(
    user_profile: dict,
    checkin: dict,
    workout_history: list,
) -> str:
    recent_workouts = workout_history[-3:]

    return f"""
User goal: {user_profile.get("goal")}
Experience level: {user_profile.get("experience_level")}
Available equipment today: {checkin.get("equipment_today")}
Time available: {checkin.get("available_time_minutes")} minutes
Energy level: {checkin.get("energy_level")}
Soreness: {checkin.get("soreness")}
Recent workouts: {recent_workouts}

Find relevant workout programming rules, recovery guidance,
exercise options, warmup/cooldown advice, and substitutions.
""".strip()


def build_knowledge_context(chunks: list) -> str:
    parts = []

    for index, chunk in enumerate(chunks, start=1):
        parts.append(
            f"""
[Retrieved chunk {index}]
Source: {chunk["source"]}
Similarity score: {chunk["score"]:.4f}

{chunk["content"]}
""".strip()
        )

    return "\n\n".join(parts)


def build_rag_debug_markdown(
    retrieval_query: str,
    retrieved_chunks: list,
) -> str:
    parts = [
        "# RAG Debug Report",
        "",
        "## Retrieval Query",
        "",
        "```text",
        retrieval_query,
        "```",
        "",
        "## Retrieved Chunks",
        "",
    ]

    for index, chunk in enumerate(retrieved_chunks, start=1):
        parts.extend(
            [
                f"### Chunk {index}",
                "",
                f"- **Source:** `{chunk['source']}`",
                f"- **Similarity score:** `{chunk['score']:.4f}`",
                "",
                "```markdown",
                chunk["content"],
                "```",
                "",
            ]
        )

    return "\n".join(parts)


def build_workout_markdown(
    workout_plan: str,
    user_profile: dict,
    checkin: dict,
    retrieved_chunks: list,
) -> str:
    sources = "\n".join(
        [
            f"- `{chunk['source']}` — score `{chunk['score']:.4f}`"
            for chunk in retrieved_chunks
        ]
    )

    return f"""
# Generated Workout Plan

## Metadata

- **Goal:** {user_profile.get("goal")}
- **Experience level:** {user_profile.get("experience_level")}
- **Available time:** {checkin.get("available_time_minutes")} minutes
- **Energy level:** {checkin.get("energy_level")}
- **Soreness:** {checkin.get("soreness")}
- **Equipment today:** {checkin.get("equipment_today")}

---

## Workout Plan

{workout_plan}

---

## Retrieved RAG Sources

{sources}
""".strip()


def generate_workout_plan(
    user_profile: dict,
    workout_history: list,
    checkin: dict,
    retrieved_chunks: list,
) -> str:
    knowledge_context = build_knowledge_context(retrieved_chunks)

    prompt = f"""
You are RepMind, an AI fitness planning assistant.

Create a safe, realistic workout for today.

Use the user's profile, recent workout history, today's check-in,
and the retrieved knowledge context.

Important rules:
- Do not ignore soreness.
- Do not recommend exercises that require unavailable equipment.
- Include warm-up, main workout, cooldown, and explanation.
- If energy is low or sleep is poor, reduce intensity or volume.
- Make the workout fit the available time.
- Use the retrieved knowledge when relevant.
- Be practical and specific.

User profile:
{json.dumps(user_profile, indent=2)}

Recent workout history:
{json.dumps(workout_history[-5:], indent=2)}

Today's check-in:
{json.dumps(checkin, indent=2)}

Retrieved knowledge:
{knowledge_context}

Return the answer in this format:

TODAY'S WORKOUT:
...

WHY THIS WORKOUT:
...

PLAN:
...

SAFETY NOTES:
...

RAG SOURCES USED:
...
""".strip()

    response = client.models.generate_content(
        model=GENERATION_MODEL,
        contents=prompt,
    )

    return response.text


def main():
    user_profile = load_json(DATA_DIR / "demo_user.json")

    workout_history_path = DATA_DIR / "workout_history.json"
    workout_history = load_json(workout_history_path)

    checkin = {
        "available_time_minutes": 45,
        "energy_level": "medium",
        "soreness": ["quads", "glutes"],
        "equipment_today": ["dumbbells", "pull-up bar"],
        "notes": "I slept okay but my legs are still sore.",
    }

    while True:
        run_dir = create_run_dir()

        retrieval_query = build_retrieval_query(
            user_profile=user_profile,
            checkin=checkin,
            workout_history=workout_history,
        )

        retrieved_chunks = retrieve_relevant_chunks(
            retrieval_query,
            top_k=5,
        )

        workout_plan = generate_workout_plan(
            user_profile=user_profile,
            workout_history=workout_history,
            checkin=checkin,
            retrieved_chunks=retrieved_chunks,
        )

        workout_markdown = build_workout_markdown(
            workout_plan=workout_plan,
            user_profile=user_profile,
            checkin=checkin,
            retrieved_chunks=retrieved_chunks,
        )

        rag_debug_markdown = build_rag_debug_markdown(
            retrieval_query=retrieval_query,
            retrieved_chunks=retrieved_chunks,
        )

        save_text(run_dir / "workout_plan.md", workout_markdown)
        save_text(run_dir / "rag_debug.md", rag_debug_markdown)
        save_json(run_dir / "rag_debug.json", retrieved_chunks)
        save_json(run_dir / "checkin.json", checkin)

        print("\n=== FINAL WORKOUT PLAN ===\n")
        print(workout_plan)

        print("\n=== FILES SAVED ===\n")
        print(f"Workout plan: {run_dir / 'workout_plan.md'}")
        print(f"RAG debug markdown: {run_dir / 'rag_debug.md'}")
        print(f"RAG debug JSON: {run_dir / 'rag_debug.json'}")
        print(f"Check-in: {run_dir / 'checkin.json'}")

        user_choice = input(
            "\nDid you do / accept this workout? "
            "[y = save to history, r = regenerate, q = quit without saving]: "
        ).strip().lower()

        if user_choice == "y":
            append_workout_to_history(
                history_path=workout_history_path,
                workout_history=workout_history,
                workout_plan=workout_plan,
                checkin=checkin,
                retrieved_chunks=retrieved_chunks,
                status="completed",
            )

            print("\nWorkout saved to workout_history.json")
            break

        elif user_choice == "r":
            print("\nRegenerating workout...\n")
            continue

        elif user_choice == "q":
            print("\nExiting without saving workout to history.")
            break

        else:
            print("\nInvalid choice. Please enter y, r, or q.")


if __name__ == "__main__":
    main()