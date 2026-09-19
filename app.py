import streamlit as st

from core.question_bank import load_questions
from core.state import create_initial_state
from core.scoring import evaluate_answer, update_state
from utils.graph_runner import get_next_question
from agents.profile_agent import generate_cognitive_profile


MAX_QUESTIONS = 10


st.set_page_config(
    page_title="Adaptive Cognitive Test",
    page_icon="🧠",
    layout="centered"
)


# --------------------------------------------------
# Load question bank
# --------------------------------------------------

questions = load_questions()


# --------------------------------------------------
# Initialize Streamlit session state
# --------------------------------------------------

if "started" not in st.session_state:
    st.session_state.started = False

if "test_state" not in st.session_state:
    st.session_state.test_state = create_initial_state()

if "current_question" not in st.session_state:
    st.session_state.current_question = None

if "last_feedback" not in st.session_state:
    st.session_state.last_feedback = None

if "waiting_for_next_question" not in st.session_state:
    st.session_state.waiting_for_next_question = False


# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("🧠 Adaptive Cognitive Test")

st.write(
    "An adaptive cognitive assessment that changes "
    "question difficulty and category based on your performance."
)


# --------------------------------------------------
# Start screen
# --------------------------------------------------

if not st.session_state.started:

    st.info(
        "You will answer 10 questions. "
        "The difficulty and category of upcoming questions "
        "will adapt based on your performance."
    )

    if st.button("🚀 Start Test"):

        st.session_state.started = True

        new_state = create_initial_state()

        graph_result = get_next_question(
            new_state
        )

        new_state["current_question"] = (
            graph_result["current_question"]
        )

        new_state["selection_reason"] = (
            graph_result["selection_reason"]
        )

        new_state["current_difficulty"] = (
            graph_result["current_difficulty"]
        )

        st.session_state.test_state = new_state
        st.session_state.last_feedback = None
        st.session_state.waiting_for_next_question = False

        st.rerun()


# --------------------------------------------------
# Completed screen
# --------------------------------------------------

elif st.session_state.test_state["completed"]:

    state = st.session_state.test_state

    profile = generate_cognitive_profile(state)

    st.success("🎉 Test completed!")

    st.header("🧠 Cognitive Profile")

    score = profile["overall"]["score"]
    total = profile["overall"]["total"]
    percentage = profile["overall"]["accuracy"]

    st.metric(
        "Overall Score",
        f"{score}/{total}"
    )

    st.metric(
        "Accuracy",
        f"{percentage:.0f}%"
    )

    st.subheader("Category Performance")

    for category, data in profile["category_performance"].items():

        st.write(
            f"**{category}:** "
            f"{data['correct']}/{data['attempts']} "
            f"({data['accuracy']:.0f}%)"
        )

    st.subheader(
        "Observed Strengths and Areas for Improvement"
    )

    if profile["strongest_categories"]:

        st.write(
            f"**Strongest observed areas:** "
            f"{', '.join(profile['strongest_categories'])}"
        )

    else:

        st.write(
            "**Strongest observed areas:** "
            "No strengths identified from this attempt."
        )

    if profile["weakest_categories"]:

        st.write(
            f"**Area(s) with the lowest observed accuracy:** "
            f"{', '.join(profile['weakest_categories'])}"
        )

    else:

        st.write(
            "**Areas for improvement:** "
            "No areas identified from this attempt."
        )

    st.divider()

    st.subheader("Response Summary")

    for answer in state["answers"]:

        status = (
            "✅ Correct"
            if answer["correct"]
            else "❌ Incorrect"
        )

        st.write(
            f"Question {answer['question_id']} — "
            f"{answer['category']} — "
            f"{answer['difficulty'].title()} — "
            f"{status}"
        )

    st.divider()

    if st.button("🔄 Take Test Again"):

        st.session_state.started = False
        st.session_state.test_state = create_initial_state()
        st.session_state.current_question = None
        st.session_state.last_feedback = None
        st.session_state.waiting_for_next_question = False

        st.rerun()


# --------------------------------------------------
# Active test
# --------------------------------------------------

else:

    state = st.session_state.test_state
    question = state["current_question"]


    # --------------------------------------------------
    # Display feedback before next question
    # --------------------------------------------------

    if st.session_state.waiting_for_next_question:

        feedback = st.session_state.last_feedback

        st.subheader("Answer Feedback")

        if feedback["correct"]:

            st.success("✅ Correct!")

        else:

            st.error("❌ Incorrect.")

            st.info(
                f"The correct answer was: "
                f"**{feedback['correct_answer']}**"
            )

        st.divider()

        if st.button("➡️ Continue to Next Question"):

            st.session_state.waiting_for_next_question = False
            st.session_state.last_feedback = None

            st.rerun()

        st.stop()


    # --------------------------------------------------
    # Safety check
    # --------------------------------------------------

    if question is None:

        st.error("No question available.")

        if st.button("Restart Test"):

            st.session_state.started = False
            st.session_state.test_state = (
                create_initial_state()
            )
            st.session_state.current_question = None
            st.session_state.last_feedback = None
            st.session_state.waiting_for_next_question = False

            st.rerun()


    else:

        question_number = (
            state["questions_answered"] + 1
        )

        st.progress(
            state["questions_answered"] /
            MAX_QUESTIONS
        )

        st.write(
            f"### Question {question_number} "
            f"of {MAX_QUESTIONS}"
        )


        # --------------------------------------------------
        # Selection explanation
        # --------------------------------------------------

        if state["selection_reason"]:

            with st.expander(
                "💡 Why was this question selected?"
            ):

                st.write(
                    state["selection_reason"]
                )


        # --------------------------------------------------
        # Question metadata
        # --------------------------------------------------

        col1, col2 = st.columns(2)

        with col1:

            st.caption(
                f"Category: {question['category']}"
            )

        with col2:

            st.caption(
                f"Difficulty: "
                f"{question['difficulty'].title()}"
            )


        st.divider()


        # --------------------------------------------------
        # Question
        # --------------------------------------------------

        st.subheader(
            question["question"]
        )


        # --------------------------------------------------
        # Answer form
        # --------------------------------------------------

        with st.form(
            key=f"question_form_{question['id']}"
        ):

            user_answer = st.radio(
                "Choose your answer:",
                question["options"]
            )

            submitted = st.form_submit_button(
                "Submit Answer"
            )


        # --------------------------------------------------
        # Process answer
        # --------------------------------------------------

        if submitted:

            # Evaluate current answer
            result = evaluate_answer(
                question,
                user_answer
            )

            # Save feedback
            st.session_state.last_feedback = {
                "correct": result["correct"],
                "correct_answer": question["answer"]
            }

            # Update adaptive state
            update_state(
                state,
                question,
                result,
                user_answer
            )


            # --------------------------------------------------
            # Check completion
            # --------------------------------------------------

            if (
                state["questions_answered"]
                >= MAX_QUESTIONS
            ):

                state["completed"] = True

                st.session_state.test_state = state

                st.session_state.waiting_for_next_question = False

                st.rerun()


            # --------------------------------------------------
            # Select next question
            # --------------------------------------------------

            else:

                graph_result = get_next_question(
                    state
                )

                state["current_question"] = (
                    graph_result["current_question"]
                )

                state["selection_reason"] = (
                    graph_result["selection_reason"]
                )

                state["current_difficulty"] = (
                    graph_result["current_difficulty"]
                )

                st.session_state.test_state = state

                # Show feedback before rendering
                # the next question
                st.session_state.waiting_for_next_question = True

                st.rerun()


# --------------------------------------------------
# Sidebar
# --------------------------------------------------

with st.sidebar:

    st.header("📊 Test Progress")

    state = st.session_state.test_state

    st.write(
        f"Questions answered: "
        f"{state['questions_answered']}/"
        f"{MAX_QUESTIONS}"
    )

    st.write(
        f"Current score: "
        f"{state['score']}"
    )

    if state["questions_answered"] > 0:

        accuracy = (
            state["score"] /
            state["questions_answered"]
        ) * 100

        st.write(
            f"Current accuracy: "
            f"{accuracy:.0f}%"
        )

    st.divider()

    st.subheader(
        "Category Attempts"
    )

    for category, attempts in (
        state["category_attempts"].items()
    ):

        st.write(
            f"{category}: {attempts}"
        )