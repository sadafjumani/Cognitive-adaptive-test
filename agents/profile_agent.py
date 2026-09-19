def generate_cognitive_profile(state):
    """
    Generate a structured cognitive profile from
    the user's completed assessment state.
    """

    score = state["score"]
    total = state["questions_answered"]

    overall_accuracy = (
        (score / total) * 100
        if total > 0
        else 0
    )

    category_performance = {}

    for category in state["category_scores"]:

        attempts = state["category_attempts"][category]
        correct = state["category_scores"][category]

        accuracy = (
            (correct / attempts) * 100
            if attempts > 0
            else 0
        )

        category_performance[category] = {
            "correct": correct,
            "attempts": attempts,
            "accuracy": round(accuracy, 1)
        }

    # Identify strongest and weakest observed categories
    attempted_categories = {
        category: data
        for category, data in category_performance.items()
        if data["attempts"] > 0
    }

    if attempted_categories:

     highest_accuracy = max(
        data["accuracy"]
        for data in attempted_categories.values()
     )

     lowest_accuracy = min(
        data["accuracy"]
        for data in attempted_categories.values()
     )
     
     if highest_accuracy > 0:
      strongest_categories = [
        category
        for category, data in attempted_categories.items()
        if data["accuracy"] == highest_accuracy
      ]
     else:
        strongest_categories = []

     if lowest_accuracy < 100:
      weakest_categories = [
        category
        for category, data in attempted_categories.items()
        if data["accuracy"] == lowest_accuracy
      ]
     else:
        weakest_categories = []

    else:

     strongest_categories = []
     weakest_categories = []

    return {
        "overall": {
            "score": score,
            "total": total,
            "accuracy": round(overall_accuracy, 1)
        },
        "category_performance": category_performance,
        "strongest_categories": strongest_categories,
        "weakest_categories": weakest_categories,
        "questions_answered": state["answers"]
    }