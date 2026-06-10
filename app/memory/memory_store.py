import json

from app.config import DATA_DIR


WORKOUT_HISTORY_PATH = DATA_DIR / "workout_history.json"
MEMORY_SUMMARY_PATH = DATA_DIR / "memory_summary.md"


def load_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path, data) -> None:
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )


def load_user_profile() -> dict:
    return load_json(DATA_DIR / "demo_user.json")


def load_workout_history() -> list:
    return load_json(WORKOUT_HISTORY_PATH)


def save_workout_history(workout_history: list) -> None:
    save_json(WORKOUT_HISTORY_PATH, workout_history)


def load_memory_summary() -> str:
    if not MEMORY_SUMMARY_PATH.exists():
        return ""

    return MEMORY_SUMMARY_PATH.read_text(encoding="utf-8")


def save_memory_summary(memory_summary: str) -> None:
    MEMORY_SUMMARY_PATH.write_text(
        memory_summary,
        encoding="utf-8",
    )