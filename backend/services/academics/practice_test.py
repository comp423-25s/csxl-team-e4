from typing import Optional, Annotated
from backend.models.academics.practice_test import AIResponse, AIRequest, OpenAPIResponse
from backend.services.openai import OpenAIService
from backend.database import Session, db_session
from backend.models.openai_test_response import OpenAITestResponse
from fastapi import Depends

class PracticeTestService:
    _session: Session
    _openai_svc: OpenAIService

    _fake_responses_db = {
        1: "Study Guide Unit 2 Topic 3",
        2: "Study Guide Unit 2 Topic 4",
        3: "Study Guide Unit 2 Topic 1"
    }

    def __init__(
        self,
        session: Annotated[Session, Depends(db_session)],
        openai_svc: Annotated[OpenAIService, Depends()],
    ):
        self._session = session
        self._openai_svc = openai_svc

    def get_response(self, response_id: int) -> Optional[AIResponse]:
        result = self._fake_responses_db.get(response_id)
        if result is None:
            return None
        return AIResponse(response_id=response_id, test=result)

    def delete_response(self, response_id: int) -> bool:
        if response_id in self._fake_responses_db:
            del self._fake_responses_db[response_id]
            return True
        return False

    def generate_test(self, req: AIRequest) -> AIResponse:
        new_id = max(self._fake_responses_db.keys(), default=0) + 1
        
        system_prompt = "You are a helpful teaching assistant generating practice test questions."

        ai_generated_test = self._openai_svc.prompt(
            system_prompt=system_prompt,
            user_prompt=req.text,
            response_model=OpenAPIResponse
        )
        
        self._fake_responses_db[new_id] = ai_generated_test
        return AIResponse(response_id=new_id, test=ai_generated_test.test)