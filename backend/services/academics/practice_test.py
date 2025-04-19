from typing import Optional, Annotated
from backend.models.academics.practice_test import (
    AIResponse,
    AIRequest,
    OpenAPIResponse,
)
from backend.services.openai import OpenAIService
from backend.database import Session, db_session
from backend.models.openai_test_response import OpenAITestResponse
from fastapi import Depends
from sqlalchemy.orm import Session as SQLAlchemySession
from backend.entities.academics.practice_test_entity import PracticeTestEntity
from sqlalchemy import select
from datetime import datetime


class PracticeTestService:
    _session: Session
    _openai_svc: OpenAIService

    def __init__(
        self,
        session: Annotated[Session, Depends(db_session)],
        openai_svc: Annotated[OpenAIService, Depends()],
    ):
        self._session = session
        self._openai_svc = openai_svc

    def get_response(self, response_id: int) -> Optional[AIResponse]:
        query = select(PracticeTestEntity).filter(
            PracticeTestEntity.resource_id == response_id
        )
        entity = self._session.scalars(query).one_or_none()

        if entity is None:
            return None
        return entity.to_response_model()

    def delete_response(self, resource_id: int) -> bool:
        entity = self._session.get(PracticeTestEntity, resource_id)
        if entity is None:
            return None
        else:
            self._session.delete(entity)
            self._session.commit()
            return True

    def generate_test(self, req: AIRequest) -> AIResponse:
        system_prompt = (
            "You are a helpful teaching assistant generating practice test questions."
        )

        ai_generated_test = self._openai_svc.prompt(
            system_prompt=system_prompt,
            user_prompt=req.text,
            response_model=OpenAPIResponse,
        )

        practice_test = PracticeTestEntity(
            user="Sally Student",
            course="Comp 110",
            user_prompt=req.text,
            test_contents=ai_generated_test.test,
            created_at=datetime.now(),
            instructor_approved=False,
        )

        self._session.add(practice_test)
        self._session.commit()
        self._session.refresh(practice_test)

        return practice_test.to_response_model()