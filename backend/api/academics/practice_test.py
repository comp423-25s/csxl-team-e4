from fastapi import APIRouter
from ...models.academics.practice_test import AIResponse, AIRequest
from backend.services.academics.practice_test import (
    make_test,
    get_AI_response,
    delete_AI_response,
)
from fastapi import HTTPException

api = APIRouter(prefix="/api/academics/practice_test")


@api.get(
    "/retrieve_response/{response_id}", tags=["Academics"], response_model=AIResponse
)
def get_response(response_id: int):
    """Retrieve a response given a response id."""
    response = get_AI_response(response_id)
    if response is None:
        raise HTTPException(status_code=404, detail="Response not found")
    return response


@api.post("/generate_test", tags=["Academics"], response_model=AIResponse)
def generate_test(req: AIRequest):
    """
    Fake AI summary endpoint.
    Takes in text and returns a dummy summary.
    """
    # Delegate to service (to be created)
    id, result = make_test(req.text, req.image, req.file)
    return AIResponse(response_id=id, test=result)


@api.delete("/delete_response/{response_id}", tags=["Academics"])
def delete_response(response_id: int):
    """Delete an AI response by ID."""
    success = delete_AI_response(response_id)
    if not success:
        raise HTTPException(status_code=404, detail="Response not found")
    return f"Response {response_id} deleted successfully"
