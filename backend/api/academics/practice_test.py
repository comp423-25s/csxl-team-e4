from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from backend.models.academics.practice_test import AIResponse, AIRequest
from backend.services.academics.practice_test import PracticeTestService

api = APIRouter(prefix="/api/academics/practice_test")


@api.get(
    "/retrieve_response/{response_id}", tags=["Academics"], response_model=AIResponse
)
def get_response(response_id: int, svc: Annotated[PracticeTestService, Depends()]):
    response = svc.get_response(response_id)
    if response is None:
        raise HTTPException(status_code=404, detail="Response not found")
    return response


@api.post("/generate_test", tags=["Academics"], response_model=AIResponse)
def generate_test(req: AIRequest, svc: Annotated[PracticeTestService, Depends()]):
    return svc.generate_test(req)


@api.delete("/delete_response/{response_id}", tags=["Academics"])
def delete_response(response_id: int, svc: Annotated[PracticeTestService, Depends()]):
    success = svc.delete_response(response_id)
    if not success:
        raise HTTPException(status_code=404, detail="Response not found")
    return f"Response {response_id} deleted successfully"
