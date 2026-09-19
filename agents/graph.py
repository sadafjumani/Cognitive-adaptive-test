from typing import TypedDict, Optional

from langgraph.graph import StateGraph, START, END

from core.question_bank import load_questions
from core.state import create_initial_state
from core.selector import select_next_question
from core.scoring import evaluate_answer, update_state


MAX_QUESTIONS = 10


class GraphState(TypedDict):
    score: int
    questions_answered: int
    current_question: Optional[dict]
    completed: bool
    selection_reason: str

    asked_questions: list
    answers: list
    recent_performance: list
    category_scores: dict
    category_attempts: dict
    confidence: float
    current_difficulty: str

    user_answer: Optional[str]
    answer_result: Optional[dict]


# --------------------------------------------------
# Initial state
# --------------------------------------------------

def initialize_test(state: GraphState):
    """
    Create the initial adaptive test state.
    """
    return create_initial_state()


# --------------------------------------------------
# Select question
# --------------------------------------------------

def select_question(state: GraphState):
    """
    Select the next question using the adaptive
    selection engine.
    """

    questions = load_questions()

    question = select_next_question(
        state,
        questions
    )

    return {
        "current_question": question,
        "selection_reason": state["selection_reason"],
        "current_difficulty": state["current_difficulty"]
    }


# --------------------------------------------------
# Evaluate answer
# --------------------------------------------------

def evaluate_user_answer(state: GraphState):
    """
    Evaluate the user's answer against the
    selected question.
    """

    question = state["current_question"]
    user_answer = state["user_answer"]

    if question is None or user_answer is None:
        return {
            "answer_result": None
        }

    result = evaluate_answer(
        question,
        user_answer
    )

    return {
        "answer_result": result
    }


# --------------------------------------------------
# Update state
# --------------------------------------------------

def update_test_state(state: GraphState):
    """
    Update the adaptive state after the user
    submits an answer.
    """

    question = state["current_question"]
    user_answer = state["user_answer"]
    result = state["answer_result"]

    if (
        question is None
        or user_answer is None
        or result is None
    ):
        return {}

    update_state(
        state,
        question,
        result,
        user_answer
    )

    completed = (
        state["questions_answered"]
        >= MAX_QUESTIONS
    )

    return {
        "score": state["score"],
        "questions_answered": state["questions_answered"],
        "asked_questions": state["asked_questions"],
        "answers": state["answers"],
        "recent_performance": state["recent_performance"],
        "category_scores": state["category_scores"],
        "category_attempts": state["category_attempts"],
        "confidence": state["confidence"],
        "completed": completed
    }


# --------------------------------------------------
# Decide whether test is complete
# --------------------------------------------------

def route_after_update(state: GraphState):
    """
    Decide whether to finish the test or select
    another adaptive question.
    """

    if state["completed"]:
        return "finish"

    return "select_question"


# --------------------------------------------------
# Decide what to do at the beginning
# --------------------------------------------------

def route_start(state: GraphState):
    """
    Decide whether this is the initial question
    or an answer-processing cycle.
    """

    if state["user_answer"] is None:
        return "select_question"

    return "evaluate_answer"


# --------------------------------------------------
# Build LangGraph workflow
# --------------------------------------------------

def build_graph():

    graph = StateGraph(GraphState)

    # Nodes
    graph.add_node(
        "select_question",
        select_question
    )

    graph.add_node(
        "evaluate_answer",
        evaluate_user_answer
    )

    graph.add_node(
        "update_state",
        update_test_state
    )

    # Initial routing
    graph.add_conditional_edges(
        START,
        route_start,
        {
            "select_question": "select_question",
            "evaluate_answer": "evaluate_answer"
        }
    )

    # Initial / next-question path
    graph.add_edge(
        "select_question",
        END
    )

    # Answer-processing path
    graph.add_edge(
        "evaluate_answer",
        "update_state"
    )

    graph.add_conditional_edges(
        "update_state",
        route_after_update,
        {
            "select_question": "select_question",
            "finish": END
        }
    )

    return graph.compile()