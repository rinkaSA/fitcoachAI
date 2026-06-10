from app.agents.state import WorkoutState
from app.rag.retriever import retrieve_relevant_chunks


def build_retrieval_query(state: WorkoutState) -> str:
    user_profile = state["user_profile"]
    checkin = state["checkin"]
    workout_history = state["workout_history"]
    memory_summary = state.get("memory_summary", "")

    recent_workouts = workout_history[-3:]

    return f"""
User goal: {user_profile.get("goal")}
Experience level: {user_profile.get("experience_level")}

Today check-in:
- Available equipment: {checkin.get("equipment_today")}
- Time available: {checkin.get("available_time_minutes")} minutes
- Energy level: {checkin.get("energy_level")}
- Soreness: {checkin.get("soreness")}
- Notes: {checkin.get("notes")}

Long-term memory:
{memory_summary}

Recent workouts:
{recent_workouts}

Find relevant workout programming rules, recovery guidance,
exercise options, warmup/cooldown advice, and substitutions.
""".strip()


def rag_agent(state: WorkoutState) -> WorkoutState:
    retrieval_query = build_retrieval_query(state)

    retrieved_chunks = retrieve_relevant_chunks(
        retrieval_query,
        top_k=5,
    )

    state["retrieval_query"] = retrieval_query
    state["retrieved_knowledge"] = retrieved_chunks

    return state