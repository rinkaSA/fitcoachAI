import json

from google import genai

from app.config import GEMINI_API_KEY, GENERATION_MODEL

client = genai.Client(api_key=GEMINI_API_KEY)


def update_memory_summary(
    old_memory_summary: str,
    new_workout_log: dict,
    user_feedback: str = "",
) -> str:
    prompt = f"""
You are updating long-term memory for an AI fitness coaching assistant.

The memory should help future workout planning.

Old memory summary:
{old_memory_summary}

New workout log:
{json.dumps(new_workout_log, indent=2)}

User feedback:
{user_feedback}

Update the memory summary.

Rules:
- Keep it concise.
- Keep only stable or useful long-term information.
- Preserve exercise preferences.
- Preserve exercise dislikes.
- Preserve recurring soreness or recovery patterns.
- Preserve useful working weights or performance signals.
- Preserve constraints that should affect future programming.
- Do not copy every workout detail.
- Do not include one-off details unless they seem important.
- Do not invent facts.
- If there is not enough new useful information, keep the memory mostly unchanged.

Return only the updated memory summary in markdown.
""".strip()

    response = client.models.generate_content(
        model=GENERATION_MODEL,
        contents=prompt,
    )

    return response.text