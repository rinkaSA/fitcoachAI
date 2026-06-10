import json
from pathlib import Path
from datetime import datetime

from app.config import DATA_DIR
from app.workflows.workout_graph import workout_graph
from app.memory.memory_store import (
    load_workout_history,
    save_workout_history,
    load_memory_summary,
    save_memory_summary,
)
from app.memory.memory_updater import update_memory_summary


GENERATED_WORKOUTS_DIR = DATA_DIR / "generated_workouts"
WORKOUT_HISTORY_PATH = DATA_DIR / "workout_history.json"


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
    run_dir = GENERATED_WORKOUTS_DIR / f"{timestamp}_candidate"
    run_dir.mkdir(parents=True, exist_ok=True)
    return run_dir


def mark_run_as_accepted(run_dir: Path) -> Path:
    accepted_dir = run_dir.with_name(
        run_dir.name.replace("_candidate", "_accepted")
    )

    run_dir.rename(accepted_dir)

    return accepted_dir


def build_rag_debug_markdown(final_state: dict) -> str:
    retrieved_chunks = final_state.get("retrieved_knowledge", [])
    retrieval_query = final_state.get("retrieval_query", "")

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


def build_workout_markdown(final_state: dict) -> str:
    user_profile = final_state["user_profile"]
    checkin = final_state["checkin"]
    workout_plan = final_state["workout_plan"]
    retrieved_chunks = final_state.get("retrieved_knowledge", [])

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


def append_workout_to_history(final_state: dict, status: str = "completed") -> dict:
    workout_history = load_workout_history()

    checkin = final_state["checkin"]
    workout_plan = final_state["workout_plan"]
    retrieved_chunks = final_state.get("retrieved_knowledge", [])

    new_entry = {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "source": "generated_langgraph_rag_plan",
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
    save_workout_history(workout_history)

    return new_entry


def save_generated_artifacts(final_state: dict, run_dir: Path) -> None:
    workout_markdown = build_workout_markdown(final_state)
    rag_debug_markdown = build_rag_debug_markdown(final_state)

    save_text(run_dir / "workout_plan.md", workout_markdown)
    save_text(run_dir / "rag_debug.md", rag_debug_markdown)
    save_json(run_dir / "rag_debug.json", final_state.get("retrieved_knowledge", []))
    save_json(run_dir / "checkin.json", final_state["checkin"])


def update_memory_after_accepted_workout(new_history_entry: dict) -> None:
    old_memory_summary = load_memory_summary()

    updated_memory_summary = update_memory_summary(
        old_memory_summary=old_memory_summary,
        new_workout_log=new_history_entry,
        user_feedback="User accepted/completed this generated workout.",
    )

    save_memory_summary(updated_memory_summary)


def generate_once(checkin: dict) -> tuple[dict, Path]:
    run_dir = create_run_dir()

    final_state = workout_graph.invoke(
        {
            "checkin": checkin,
        }
    )

    save_generated_artifacts(
        final_state=final_state,
        run_dir=run_dir,
    )

    return final_state, run_dir


def main():
    checkin = {
        "available_time_minutes": 45,
        "energy_level": "medium",
        "soreness": ["quads", "glutes"],
        "equipment_today": ["dumbbells", "pull-up bar"],
        "notes": "I slept okay but my legs are still sore.",
    }

    while True:
        final_state, run_dir = generate_once(checkin)

        print("\n=== FINAL WORKOUT PLAN ===\n")
        print(final_state["workout_plan"])

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
            new_history_entry = append_workout_to_history(
                final_state=final_state,
                status="completed",
            )

            update_memory_after_accepted_workout(new_history_entry)

            accepted_dir = mark_run_as_accepted(run_dir)

            print("\nWorkout saved to workout_history.json")
            print("Memory summary updated.")
            print(f"Accepted workout files: {accepted_dir}")
            break

        if user_choice == "r":
            print("\nRegenerating workout...\n")
            continue

        if user_choice == "q":
            print("\nExiting without saving workout to history.")
            break

        print("\nInvalid choice. Please enter y, r, or q.")


if __name__ == "__main__":
    main()