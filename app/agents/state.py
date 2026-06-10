from typing import TypedDict, List, Dict, Any


class WorkoutState(TypedDict, total=False):
    checkin: Dict[str, Any]

    user_profile: Dict[str, Any]
    workout_history: List[Dict[str, Any]]
    memory_summary: str

    retrieved_knowledge: List[Dict[str, Any]]

    workout_plan: str