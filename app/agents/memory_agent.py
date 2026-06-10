from app.agents.state import WorkoutState
from app.memory.memory_store import (
    load_user_profile,
    load_workout_history,
    load_memory_summary,
)


def memory_agent(state: WorkoutState) -> WorkoutState:
    """
    Loads persistent user context into the temporary LangGraph state.

    This agent does not update memory.
    It only reads:
    - user profile
    - workout history
    - long-term memory summary

    Later agents use this information to personalize the workout plan.
    """

    user_profile = load_user_profile()
    workout_history = load_workout_history()
    memory_summary = load_memory_summary()

    state["user_profile"] = user_profile
    state["workout_history"] = workout_history
    state["memory_summary"] = memory_summary

    return state