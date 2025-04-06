from typing import Optional
from backend.models.academics.practice_test import AIResponse

fake_responses_db = {}

def retrieve_response(response_id: int) -> Optional[AIResponse]:
    """Retrieve a specific AI response by ID."""
    return fake_responses_db.get(response_id)

def delete_response(response_id: int) -> bool:
    """Delete an AI response by ID."""
    if response_id in fake_responses_db:
        del fake_responses_db[response_id]
        return True
    return False

def generate_test(text, image, file) -> str:
    new_id = max(fake_responses_db.keys()) + 1
    test = "1. T/F is this fully implemented? Answer: False"
    fake_responses_db[new_id] = test
    return test