import pytest
from unittest.mock import MagicMock

from .fixtures import practice_test_svc, openai_svc_mock, client

from backend.services.academics.practice_test import PracticeTestService
from backend.services.openai import OpenAIService
from backend.models.academics.practice_test import AIResponse, AIRequest
from backend.api.academics.practice_test import api
from datetime import datetime
from fastapi.testclient import TestClient

#Unit Tests

def test_generate_test(practice_test_svc: PracticeTestService, openai_svc_mock: OpenAIService):
    openai_svc_mock.prompt.return_value = MagicMock(test="Generated Test Content")
    request = AIRequest(prompt="Sample Question", formats=["Multiple choice"], resource_ids=[1])
    response = practice_test_svc.generate_test(request)
    
    assert response is not None
    assert response.response_id > 0
    assert response.user == "Sally Student"
    assert response.course == "COMP 110"
    assert "Sample Question" in response.user_prompt
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

def test_delete_response(practice_test_svc: PracticeTestService):
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

    success = service.delete_response(1)
    assert success is True

def test_delete_response_not_found(practice_test_svc: PracticeTestService):
    success = practice_test_svc.delete_response(999)
    assert success is False

#Integration Tests

def test_get_route(client: TestClient, practice_test_svc: PracticeTestService):
    practice_test_svc.get_response = MagicMock(return_value=AIResponse(
        response_id=1,
        user="Sally Student",
        course="COMP 110",
        user_prompt="Practice Test",
        test_contents="Test Content",
        created_at=datetime.now(),
        instructor_approved=False
    ))
    
    response = client.get("/api/academics/practice_test/retrieve_response/1")
    assert response.status_code == 200

def test_get_route_error(client: TestClient, practice_test_svc: PracticeTestService):
    practice_test_svc.get_response = MagicMock(return_value=None)
    
    response = client.get("/api/academics/practice_test/retrieve_response/999")
    assert response.status_code == 404

def test_post_route(client: TestClient, practice_test_svc: PracticeTestService):
    practice_test_svc.generate_test = MagicMock(return_value=AIResponse(
        response_id=1,
        user="Sally Student",
        course="COMP 110",
        user_prompt="Practice Test",
        test_contents="Test Content",
        created_at=datetime.now(),
        instructor_approved=False
    ))
    
    request_data = {"prompt": "Sample Question", "formats":["Multiple Choice"], "resource_ids": [1]}
    response = client.post("/api/academics/practice_test/generate_test", json=request_data)
    
    assert response.status_code == 200

def test_delete_route(client: TestClient, practice_test_svc: PracticeTestService):
    practice_test_svc.delete_response = MagicMock(return_value=True)
    
    response = client.delete("/api/academics/practice_test/delete_response/1")
    assert response.status_code == 200

def test_delete_route_error(client: TestClient, practice_test_svc: PracticeTestService):
    practice_test_svc.delete_response = MagicMock(return_value=False)
    
    response = client.delete("/api/academics/practice_test/delete_response/999")
    assert response.status_code == 404