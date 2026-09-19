import json


def load_questions():
    with open("data/questions.json", "r", encoding="utf-8") as file:
        return json.load(file)