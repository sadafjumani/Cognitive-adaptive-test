def create_initial_state():
    return {
        "current_question": None,

        "current_difficulty": "medium",

        "score": 0,

        "questions_answered": 0,

        "asked_questions": [],

        "answers": [],

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

        "recent_performance": [],

        "confidence": 0.5,

        "selection_reason": "",

        "completed": False
    }