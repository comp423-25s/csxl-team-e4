import pytest
from unittest.mock import MagicMock

from .fixtures import resource_svc, resource_client

from backend.services.academics.resource import ResourceService
from backend.models.academics.resource import Resource
from backend.entities.academics.resource_entity import ResourceEntity
from backend.api.academics.resource import api
from fastapi.testclient import TestClient
import io


#Unit Tests

def test_delete_resource():
    mock_session = MagicMock()

    mock_entity = MagicMock()
    mock_session.scalars.return_value.one_or_none.return_value = mock_entity

    service = ResourceService(session=mock_session)

    success = service.delete(1)

    assert success is True
    mock_session.delete.assert_called_once_with(mock_entity)
    mock_session.commit.assert_called_once()


def test_delete_resource_not_found():
    mock_session = MagicMock()
    mock_session.scalars.return_value.one_or_none.return_value = None

    service = ResourceService(session=mock_session)

    success = service.delete(999)

    assert success is False
    mock_session.commit.assert_not_called()


def test_get_all_resources():
    mock_session = MagicMock()
    fake_entity = MagicMock()
    fake_entity.to_model.return_value = Resource(
        id=1, title="Syllabus", file_name="syllabus.pdf", ta_upload=False
    )
    mock_session.scalars.return_value.all.return_value = [fake_entity]

    service = ResourceService(session=mock_session)
    resources = service.get_all_resources()

    assert len(resources) == 1
    assert resources[0].title == "Syllabus"
    assert isinstance(resources[0], Resource)


def test_get_resource_by_id():
    mock_session = MagicMock()
    fake_entity = MagicMock(id=2, ta_upload=True, title="Lecture 01", file_name="Chapter1.pdf", course_id="comp110")
    mock_session.scalars.return_value.one_or_none.return_value = fake_entity

    service = ResourceService(session=mock_session)
    entity = service.get_resource_by_id(2)

    assert entity.id == 2
    assert entity.ta_upload == True
    assert entity.title == "Lecture 01"
    assert entity.file_name == "Chapter1.pdf"
    assert entity.course_id == "comp110"


def test_get_resource_by_id_not_found():
    mock_session = MagicMock()
    mock_session.scalars.return_value.one_or_none.return_value = None

    service = ResourceService(session=mock_session)
    assert service.get_resource_by_id(999) is None


def test_get_resources_by_course_id():
    mock_session = MagicMock()

    # course entity first query
    course_entity = MagicMock(id="comp110")
    mock_session.scalars.return_value.one_or_none.side_effect = [course_entity]

    # follow‑up query returns list of resource entities
    res_entity = MagicMock()
    res_entity.to_model.return_value = Resource(
        id=3, title="Slides", file_name="slides.pdf", ta_upload=True
    )
    mock_session.scalars.return_value.all.return_value = [res_entity]

    service = ResourceService(session=mock_session)
    models = service.get_resources_by_course_id("comp110")

    assert len(models) == 1
    assert models[0].id == 3
    assert models[0].title == "Slides"
    assert models[0].file_name == "slides.pdf"
    assert models[0].ta_upload is True


def test_create_new_resource():
    mock_session = MagicMock()

    service = ResourceService(session=mock_session)
    new_entity = service.create_new_resource(
        title="HW 1", file_name="hw1.pdf", course_id="comp110", file_blob=b"123"
    )

    # session.add / commit / refresh happen exactly once
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()

    # Method returns whatever SQLAlchemy would give back
    assert new_entity == mock_session.refresh.call_args.args[0]

#Integration tests

def test_get_all_route(resource_client: TestClient, resource_svc):
    resource_svc.get_all_resources = MagicMock(return_value=[
        Resource(id=1, title="Syllabus", file_name="syllabus.pdf", ta_upload=False)
    ])

    resp = resource_client.get("/api/academics/resources/")
    assert resp.status_code == 200
    assert resp.json()[0]["title"] == "Syllabus"


def test_get_by_course_route(resource_client: TestClient, resource_svc):
    resource_svc.get_resources_by_course_id = MagicMock(return_value=[
        Resource(id=1, title="Slides", file_name="slides.pdf", ta_upload=True)
    ])

    resp = resource_client.get("/api/academics/resources/", params={"course_id": "comp110"})
    assert resp.status_code == 200
    assert resp.json()[0]["file_name"] == "slides.pdf"


def test_delete_route_success(resource_client: TestClient, resource_svc):
    resource_svc.delete = MagicMock(return_value=True)

    resp = resource_client.delete("/api/academics/resources/1")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Resource deleted successfully"


def test_delete_route_error(resource_client: TestClient, resource_svc):
    resource_svc.delete = MagicMock(return_value=False)

    resp = resource_client.delete("/api/academics/resources/999")
    assert resp.status_code == 404


def test_download_route_success(resource_client: TestClient, resource_svc):
    mock_entity = MagicMock(
        file_name="notes.pdf",
        file_data=b"%PDF-1.4 FAKE",
    )
    resource_svc.get_resource_by_id = MagicMock(return_value=mock_entity)

    resp = resource_client.get("/api/academics/resources/1/download")
    assert resp.status_code == 200
    assert resp.headers["content-disposition"].startswith("attachment; filename=notes.pdf")
    assert resp.content.startswith(b"%PDF")


def test_download_route_error(resource_client: TestClient, resource_svc):
    resource_svc.get_resource_by_id = MagicMock(return_value=None)

    resp = resource_client.get("/api/academics/resources/123/download")
    assert resp.status_code == 404


def test_upload_route(resource_client: TestClient, resource_svc):
    resource_svc.create_new_resource = MagicMock()

    data = {"title": "Lecture 02", "file_name": "lec02.pdf", "course_id": "COMP110"}
    files = {"file": ("lec02.pdf", io.BytesIO(b"dummy pdf"), "application/pdf")}

    resp = resource_client.post("/api/academics/resources/upload", data=data, files=files)
    assert resp.status_code == 200
    assert resp.json()["message"] == "Upload successful"
    resource_svc.create_new_resource.assert_called_once()
