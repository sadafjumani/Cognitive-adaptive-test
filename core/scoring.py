def evaluate_answer(question, user_answer):
    """
    Check whether the user's answer is correct.
    """

    correct = user_answer == question["answer"]

    return {
        "correct": correct,
        "points": 1 if correct else 0
    }


def update_state(state, question, result, user_answer):
    """
    Update the test state after the user answers a question.
    """
    if question["id"] in state["asked_questions"]: 
        return state

    category = question["category"]

    # Update total questions answered
    state["questions_answered"] += 1

    # Update total score
    if result["correct"]:
        state["score"] += 1
        state["category_scores"][category] += 1

    # Track number of attempts in this category
    state["category_attempts"][category] += 1

    # Store recent performance
    state["recent_performance"].append(result["correct"])
    
    recent = state["recent_performance"][-3:]

    if recent:
        state["confidence"] = round(
            sum(recent) / len(recent),
            2
        )

    # Store detailed answer information
    state["answers"].append({
        "question_id": question["id"],
        "category": category,
        "difficulty": question["difficulty"],
        "user_answer": user_answer,
        "correct": result["correct"]
    })

    # Remember that this question has already been used
    state["asked_questions"].append(question["id"])

    return state