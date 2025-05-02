import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from backend.services.academics.resource import ResourceService


# Unit Tests for ResourceService
def test_delete_found():
    session = MagicMock()
    mock_resource = MagicMock()

    # Mock the behavior of the session to ret a resource entity
    session.scalars.return_value.one_or_none.return_value = mock_resource

    svc = ResourceService(session)
    result = svc.delete(1)

    assert result is True
    session.delete.assert_called_once_with(mock_resource)
    session.commit.assert_called_once()

def test_delete_not_found():
    session = MagicMock()
    session.scalars.return_value.one_or_none.return_value = None

    svc = ResourceService(session)
    result = svc.delete(999)

    assert result is False

def test_get_all_resources():
    session = MagicMock()
    mock_entity = MagicMock()
    mock_entity.to_model.return_value = "model"
    session.scalars.return_value.all.return_value = [mock_entity]

    svc = ResourceService(session)
    result = svc.get_all_resources()

    assert result == ["model"]

def test_get_resource_by_id_found():
    session = MagicMock()
    session.scalars.return_value.one_or_none.return_value = "entity"

    svc = ResourceService(session)
    result = svc.get_resource_by_id(1)

    assert result == "entity"

def test_get_resource_by_id_not_found():
    session = MagicMock()
    session.scalars.return_value.one_or_none.return_value = None

    svc = ResourceService(session)
    result = svc.get_resource_by_id(999)

    assert result is None

def test_get_resources_by_course_id():
    session = MagicMock()
    
    mock_course = MagicMock()
    mock_course.id = 123
    session.scalars.side_effect = [
        MagicMock(one_or_none=MagicMock(return_value=mock_course)),
        MagicMock(all=MagicMock(return_value=[MagicMock(to_model=MagicMock(return_value="model"))]))
    ]

    svc = ResourceService(session)
    result = svc.get_resources_by_course_id("COMP 110")

    assert result == ["model"]

def test_create_new_resource():
    session = MagicMock()
    session.refresh.side_effect = lambda x: x  # simulate refresh

    svc = ResourceService(session)
    session.add.side_effect = lambda x: setattr(x, "id", 1)

    # PDFCONTENT is just mock binary data
    result = svc.create_new_resource("Title", "file.pdf", "COMP 110", b"PDFCONTENT")

    session.add.assert_called_once()
    session.commit.assert_called_once()
    session.refresh.assert_called_once()
    assert result.title == "Title"