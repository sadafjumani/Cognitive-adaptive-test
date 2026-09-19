from agents.graph import build_graph

graph = build_graph()

# Start with a fresh adaptive state
initial_state = {
    "score": 0,
    "questions_answered": 0,
    "current_question": None,
    "completed": False,
    "selection_reason": "",
    "asked_questions": [],
    "answers": [],
    "recent_performance": [],
    "category_scores": {
        "Logical Reasoning": 0,
        "Numerical Reasoning": 0,
        "Pattern Recognition": 0,
        "Verbal Reasoning": 0
    },
    "category_attempts": {
        "Logical Reasoning": 0,
        "Numerical Reasoning": 0,
        "Pattern Recognition": 0,
        "Verbal Reasoning": 0
    },
    "confidence": 0.5,
    "current_difficulty": "medium",

    # First simulated answer
    "user_answer": "Ravi is a graduate",
    "answer_result": None
}

result = graph.invoke(initial_state)

print("LangGraph adaptive test completed!")

print("\nFinal state:")
print("Score:", result["score"])
print("Questions answered:", result["questions_answered"])
print("Asked questions:", result["asked_questions"])
print("Recent performance:", result["recent_performance"])
print("Category scores:", result["category_scores"])
print("Category attempts:", result["category_attempts"])