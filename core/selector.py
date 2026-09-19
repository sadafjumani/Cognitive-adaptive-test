from agents.llm_agent import generate_selection_explanation

def get_recent_accuracy(state):
    """
    Calculate accuracy using the user's
    most recent three answers.
    """

    recent = state["recent_performance"][-3:]

    if not recent:
        return 0.5

    return sum(recent) / len(recent)


def choose_difficulty(state):
    """
    Choose the next difficulty based on
    the user's recent adaptive confidence.
    """

    confidence = state["confidence"]

    if confidence >= 0.75:
        return "hard"

    elif confidence <= 0.40:
        return "easy"

    else:
        return "medium"

def choose_category(state):
    """
    Choose the category to test next.
    """

    attempts = state["category_attempts"]
    scores = state["category_scores"]

    categories = list(attempts.keys())

    # First make sure all categories are tested
    least_attempted = min(
        categories,
        key=lambda category: attempts[category]
    )

    # After every category has been attempted,
    # focus on the category with the lowest accuracy.
    if all(attempts[c] > 0 for c in categories):

        weakest = min(
            categories,
            key=lambda category:
            scores[category] / attempts[category]
        )

        return weakest

    return least_attempted


def select_next_question(state, questions):
    """
    Select an unused question based on adaptive
    difficulty and category.

    The selector first tries to match both the
    target difficulty and category. If that is not
    possible, it keeps the target difficulty but
    changes category. If the target difficulty is
    exhausted, it chooses the closest available
    difficulty while avoiding repeated questions.
    """

    target_difficulty = choose_difficulty(state)
    target_category = choose_category(state)

    # --------------------------------------------------
    # 1. Exact match: difficulty + category
    # --------------------------------------------------

    candidates = [
        q for q in questions
        if q["difficulty"] == target_difficulty
        and q["category"] == target_category
        and q["id"] not in state["asked_questions"]
    ]

    # --------------------------------------------------
    # 2. Same difficulty, different category
    # --------------------------------------------------

    if not candidates:

        candidates = [
            q for q in questions
            if q["difficulty"] == target_difficulty
            and q["id"] not in state["asked_questions"]
        ]

    # --------------------------------------------------
    # 3. Target difficulty exhausted
    # Choose the closest available difficulty.
    # --------------------------------------------------

    if not candidates:

        difficulty_order = {
            "easy": 0,
            "medium": 1,
            "hard": 2
        }

        target_level = difficulty_order[target_difficulty]

        unused_questions = [
            q for q in questions
            if q["id"] not in state["asked_questions"]
        ]

        if unused_questions:

            question = min(
                unused_questions,
                key=lambda q: abs(
                    difficulty_order[q["difficulty"]]
                    - target_level
                )
            )

            candidates = [question]

    # --------------------------------------------------
    # 4. No questions remaining
    # --------------------------------------------------

    if not candidates:
        return None

    question = candidates[0]

    state["current_difficulty"] = question["difficulty"]

    recent_accuracy = get_recent_accuracy(state)

    attempts = state["category_attempts"][question["category"]]
    correct = state["category_scores"][question["category"]]

    category_accuracy = (
       correct / attempts
       if attempts > 0
       else None
   )


# --------------------------------------------------
# Explain why this category was selected
# --------------------------------------------------

    all_attempts = state["category_attempts"]

    if not all_attempts:
       category_reason = "No category history was available."

    elif not all(
       all_attempts[c] > 0
       for c in all_attempts
    ):
      category_reason = (
        "The category was selected to maintain balanced "
        "coverage of the cognitive categories."
      )

    else:

      category_accuracies = {}

      for category in all_attempts:

        category_attempts = all_attempts[category]
        category_correct = state["category_scores"][category]

        if category_attempts > 0:
            category_accuracies[category] = (
                category_correct / category_attempts
            )

      lowest_accuracy = min(
        category_accuracies.values()
      )

      weakest_categories = [
        category
        for category, accuracy in category_accuracies.items()
        if accuracy == lowest_accuracy
      ]

      if question["category"] in weakest_categories:

        category_reason = (
            f"{question['category']} was selected because "
            f"it currently has the lowest observed accuracy."
        )

      else:

        category_reason = (
            "The category was selected to maintain balanced "
            "coverage because no category currently has a "
            "lower observed accuracy."
        )


    state["selection_reason"] = generate_selection_explanation(
        question["difficulty"],
        question["category"],
        recent_accuracy,
        category_accuracy,
        category_reason
   )
    return question