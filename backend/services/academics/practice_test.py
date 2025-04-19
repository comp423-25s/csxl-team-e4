from typing import List, Optional, Annotated
import pymupdf

from backend.entities.academics.resource_entity import ResourceEntity
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
        resource_txt = self.resources_to_text(req.resource_ids)
        format_string = ", ".join(req.formats)
        system_prompt = (
            "You are a helpful teaching assistant generating practice test questions using the provided user input. Output the questions in clean LaTeX format, along with an answer key section at the end. "
        )
        user_prompt = f"""
        Make sure you include the full LaTex boilerplate in your response.
        The test should have the following format(s): {format_string}.
        Generate a test with the following instructions: {req.prompt}.
        The test should factor in information from the following resources: {resource_txt}

        """

        ai_generated_test = self._openai_svc.prompt(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            response_model=OpenAPIResponse,
        )

        practice_test = PracticeTestEntity(
            user="Sally Student",
            course="COMP 110",
            user_prompt=user_prompt,
            test_contents=ai_generated_test.test,
            created_at=datetime.now(),
            instructor_approved=False,
        )

        self._session.add(practice_test)
        self._session.commit()
        self._session.refresh(practice_test)

        return practice_test.to_response_model()

    def clean_latex(self, text:  str) -> str:
        cleaned = text.replace("\\\\", "\\")
        cleaned = cleaned.replace("“", '"').replace("”", '"').replace("’", "'")
        cleaned = cleaned.replace("\\n", "\n")
        return cleaned
    
    def extract_text_from_blob(self, blob: bytes) -> str:
        """Helper function to extract text from a PDF blob"""
        text = ""
        # parses the blob as a PDF file
        with pymupdf.open(stream=blob, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
            return text
        
    def resources_to_text(self, resource_ids: List[int]):
        """Actually extract text from the selected resources"""
        # run a sql query to get the resources selected from our table, then run the helper method on the file_data (blob)
        selected = select(ResourceEntity).where(ResourceEntity.id.in_(resource_ids))
        resources = self._session.scalars(selected).all()
        
        resource_text = []
        for resource in resources:
            text = self.extract_text_from_blob(resource.file_data)
            resource_text.append(f"=== {resource.title} ===\n{text}")
        return "\n\n".join(resource_text)



