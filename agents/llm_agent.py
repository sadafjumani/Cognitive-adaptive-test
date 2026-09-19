import os

from dotenv import load_dotenv
from google import genai


load_dotenv()


def generate_fallback_explanation(
    difficulty,
    category,
    recent_accuracy,
    category_accuracy
):
    """
    Deterministic fallback used when the Gemini API
    is unavailable or fails.
    """

    if recent_accuracy >= 0.75:
        performance = "recent performance has been strong"
    elif recent_accuracy <= 0.40:
        performance = "recent performance has been weaker"
    else:
        performance = "recent performance has been mixed"

    if category_accuracy is None:
        category_text = (
            f"{category} has not been assessed much yet"
        )
    else:
        category_text = (
            f"{category} currently has "
            f"{category_accuracy:.0%} accuracy"
        )

    return (
        f"Selected a {difficulty} {category} question because "
        f"{performance}, and {category_text}."
    )


def generate_selection_explanation(
    difficulty,
    category,
    recent_accuracy,
    category_accuracy,
    category_reason
):
    """
    Generate a short explanation using Gemini.

    If the Gemini API is unavailable or fails,
    automatically use the deterministic fallback.
    """

    fallback = generate_fallback_explanation(
        difficulty,
        category,
        recent_accuracy,
        category_accuracy
    )
    fallback = (
      f"{fallback} {category_reason}"
    )

    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return fallback

    try:
        client = genai.Client(
            api_key=api_key
        )

        category_status = (
            f"{category_accuracy:.0%} accuracy"
            if category_accuracy is not None
            else "not assessed yet"
        )

        prompt = f"""
You are explaining an adaptive cognitive test's
question-selection decision.

The system selected:
- Difficulty: {difficulty}
- Category: {category}
- Recent accuracy: {recent_accuracy:.0%}
- Category accuracy: {category_status}
- Category selection reason: {category_reason}

Write ONE short sentence explaining why this question
was selected.

Only describe observable test-state information.
Do not make claims about intelligence, personality,
or cognitive ability.
"""

        response = client.models.generate_content(
            model="gemini-3.6-flash",
            contents=prompt
        )

        explanation = response.text.strip()

        if explanation:
            return explanation

        return fallback

    except Exception:
        return fallback