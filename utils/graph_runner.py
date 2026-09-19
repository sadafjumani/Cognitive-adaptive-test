from agents.graph import build_graph


adaptive_graph = build_graph()


def prepare_graph_state(state):
    """
    Convert the Streamlit test state into the state
    expected by LangGraph.
    """

    return {
        "score": state["score"],
        "questions_answered": state["questions_answered"],
        "current_question": state["current_question"],
        "completed": state["completed"],
        "selection_reason": state["selection_reason"],
        "asked_questions": state["asked_questions"],
        "answers": state["answers"],
        "recent_performance": state["recent_performance"],
        "category_scores": state["category_scores"],
        "category_attempts": state["category_attempts"],
        "confidence": state["confidence"],
        "current_difficulty": state["current_difficulty"],
        "user_answer": None,
        "answer_result": None
    }


def get_next_question(state):
    """
    Run the LangGraph workflow to select
    the next adaptive question.
    """

    graph_state = prepare_graph_state(state)

    result = adaptive_graph.invoke(
        graph_state
    )

    return result


def process_answer(state, user_answer):
    """
    Run the LangGraph workflow to evaluate
    the user's answer and update adaptive state.
    """

    graph_state = prepare_graph_state(state)

    graph_state["user_answer"] = user_answer

    result = adaptive_graph.invoke(
        graph_state
    )

    return result