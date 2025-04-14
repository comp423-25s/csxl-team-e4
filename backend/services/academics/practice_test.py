from typing import Optional, Tuple, Any
from backend.models.academics.practice_test import AIResponse

# fake_responses_db = {}
fake_responses_db = {
    1: "Study Guide Unit 2 Topic 3",
    2: "Study Guide Unit 2 Topic 4",
    3: "Study Guide Unit 2 Topic 1",
}

new_fake_responses_db = {
    1: {
        "test": "What is a class?\nExplain inheritance in OOP.\nWrite a basic Python class.",
        "prompt": "Generate a test on Python classes and inheritance",
        "topics": ["Classes", "Inheritance", "Python"],
        "format": "MCQ, Short Answer, Code Writing",
    },
    2: {
        "test": "Define Big-O notation.\nAnalyze time complexity for sorting algorithms.",
        "prompt": "Make a test on algorithm analysis",
        "topics": ["Big-O", "Sorting", "Complexity"],
        "format": "MCQ, Short Answer",
    },
}


def get_AI_response(response_id: int) -> Optional[AIResponse]:
    """Retrieve a specific AI response by ID."""
    return fake_responses_db.get(response_id)


def delete_AI_response(response_id: int) -> bool:
    """Delete an AI response by ID."""
    if response_id in fake_responses_db:
        del fake_responses_db[response_id]
        return True
    return False


def make_test(
    text: str, image: Optional[Any] = None, file: Optional[Any] = None
) -> Tuple[int, str]:
    new_id = max(fake_responses_db.keys(), default=0) + 1
    test = "1. What is recursion?\n2. Explain dependency injection.\n3. Identify Factory vs Abstract Factory."
    fake_responses_db[new_id] = {
        "test": test,
        "prompt": text,
        "topics": [
            "Dependency Injection (DI)",
            "Design Patterns",
            "Recursion",
        ],  # Can be dynamic later
        "format": "MCQ, Practical Application, Code Writing, Short Answer, Code Tracing",
    }
    return new_id, test
