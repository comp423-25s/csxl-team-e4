import pytest
from unittest.mock import MagicMock

from .fixtures import practice_test_svc, openai_svc_mock

from backend.services.academics.practice_test import PracticeTestService
from backend.services.openai import OpenAIService
from backend.models.academics.practice_test import AIResponse, AIRequest
from backend.api.academics.practice_test import api
from datetime import datetime

def test_generate_test(practice_test_svc: PracticeTestService, openai_svc_mock: OpenAIService):
    openai_svc_mock.prompt.return_value = MagicMock(test="Generated Test Content")
    request = AIRequest(text="Sample Question")
    response = practice_test_svc.generate_test(request)
    
    assert response is not None
    assert response.response_id > 0
    assert response.user == "Sally Student"
    assert response.course == "COMP 110"
    assert response.user_prompt == "Sample Question"
    assert response.test_contents == "Generated Test Content"
    assert response.created_at is not None
    assert response.instructor_approved == False
    assert isinstance(response, AIResponse)


def test_get_response(practice_test_svc: PracticeTestService):
    mock_session = MagicMock()
    mock_openai_svc = MagicMock()

    # Mock the entity and its to_response_model
    mock_entity = MagicMock()
    mock_entity.to_response_model.return_value = AIResponse(
        response_id=1,
        user="Sally Student",
        course="COMP 110",
        user_prompt="Practice Test",
        test_contents="Test Content",
        created_at=datetime.now(),
        instructor_approved=False
    )

    mock_session.scalars.return_value.one_or_none.return_value = mock_entity

    service = PracticeTestService(session=mock_session, openai_svc=mock_openai_svc)
    

    response = service.get_response(1)
    assert response is not None
    assert response.response_id == 1
    assert response.user == "Sally Student"
    assert response.course == "COMP 110"
    assert response.user_prompt == "Practice Test"
    assert response.test_contents == "Test Content"
    assert response.created_at is not None
    assert response.instructor_approved == False
    assert isinstance(response, AIResponse)

def test_get_response_not_found(practice_test_svc: PracticeTestService):
    response = practice_test_svc.get_response(999)
    assert response is None

