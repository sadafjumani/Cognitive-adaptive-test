from core.state import create_initial_state
from agents.profile_agent import generate_cognitive_profile


state = create_initial_state()

# Simulate some completed test results
state["score"] = 6
state["questions_answered"] = 10

state["category_scores"] = {
    "Logical Reasoning": 1,
    "Numerical Reasoning": 2,
    "Pattern Recognition": 2,
    "Verbal Reasoning": 1
}

state["category_attempts"] = {
    "Logical Reasoning": 3,
    "Numerical Reasoning": 3,
    "Pattern Recognition": 2,
    "Verbal Reasoning": 2
}

state["answers"] = []

profile = generate_cognitive_profile(state)

print("Profile generation successful!")

print("\nOverall:")
print(profile["overall"])

print("\nCategory performance:")
for category, data in profile["category_performance"].items():
    print(category, ":", data)

print("\nStrongest category:")
print(profile["strongest_category"])

print("\nWeakest category:")
print(profile["weakest_category"])