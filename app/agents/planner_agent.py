import json

from google import genai

from app.config import GEMINI_API_KEY, GENERATION_MODEL
from app.agents.state import WorkoutState

client = genai.Client(api_key=GEMINI_API_KEY)


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


def planner_agent(state: WorkoutState) -> WorkoutState:
    user_profile = state["user_profile"]
    workout_history = state["workout_history"]
    checkin = state["checkin"]
    memory_summary = state.get("memory_summary", "")
    retrieved_knowledge = state["retrieved_knowledge"]

    knowledge_context = build_knowledge_context(retrieved_knowledge)

    prompt = f"""
You are FitcoachAI, an AI fitness planning assistant.

Create a safe, realistic workout for today.

Use the user's profile, recent workout history, long-term memory,
today's check-in, and retrieved knowledge context.

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

Long-term memory:
{memory_summary}

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

    state["workout_plan"] = response.text

    return state