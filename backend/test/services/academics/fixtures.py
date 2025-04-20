"""Fixtures used for testing the Courses Services."""

import pytest
from unittest.mock import create_autospec
from sqlalchemy.orm import Session

from ....services.academics.section_member import SectionMemberService
from ....services import PermissionService
from ....services.academics import TermService, CourseService, SectionService
from ....services.academics.course_site import CourseSiteService
from backend.services.academics.practice_test import PracticeTestService
from backend.services.openai import OpenAIService
from fastapi.testclient import TestClient
from backend.api.academics.practice_test import api
from fastapi import FastAPI

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"


@pytest.fixture()
def permission_svc(session: Session):
    """PermissionService fixture."""
    return PermissionService(session)


@pytest.fixture()
def term_svc(session: Session, permission_svc: PermissionService):
    """TermService fixture."""
    return TermService(session, permission_svc)


@pytest.fixture()
def course_svc(session: Session, permission_svc: PermissionService):
    """CourseService fixture."""
    return CourseService(session, permission_svc)


@pytest.fixture()
def section_svc(session: Session, permission_svc: PermissionService):
    """SectionService fixture."""
    return SectionService(session, permission_svc)


@pytest.fixture()
def section_member_svc(session: Session, permission_svc: PermissionService):
    """SectionMemberService fixture."""
    return SectionMemberService(session, permission_svc)


@pytest.fixture()
def course_site_svc(session: Session):
    """CourseSiteService fixture."""
    return CourseSiteService(session)

@pytest.fixture()
def openai_svc_mock():
    """Mock OpenAIService"""
    return create_autospec(OpenAIService)

@pytest.fixture()
def practice_test_svc(session: Session, openai_svc_mock: OpenAIService):
    """PracticeTestService fixture"""
    return PracticeTestService(session, openai_svc_mock)

@pytest.fixture()
def client(practice_test_svc: PracticeTestService):
    """Fixture for setting up TestClient with mocked service."""
    app = FastAPI()
    app.include_router(api)
    return TestClient(app)