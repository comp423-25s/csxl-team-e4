import pytest
from sqlalchemy.orm import Session
from backend.models.academics.practice_test import (
    AIResponse,
    AIRequest,
    OpenAPIResponse,
)
from backend.entities.academics.practice_test_entity import PracticeTestEntity
from datetime import datetime
from ..reset_table_id_seq import reset_table_id_seq


def insert_fake_data(session: Session):
    entities = []
    practice_test = PracticeTestEntity(
        user="Sally Student",
        course="Comp 110",
        user_prompt="Generate a practice test for Data Structures",
        test_contents="Fake test",
        created_at=datetime.now(),
        instructor_approved=False,
    )
    session.add(practice_test)
    entities.append(practice_test)

    practice_test_2 = PracticeTestEntity(
        user="Sally Student",
        course="Comp 110",
        user_prompt="Generate a practice test for Data Structures",
        test_contents="Fake test 2",
        created_at=datetime.now(),
        instructor_approved=False,
    )
    session.add(practice_test)
    session.add(practice_test_2)
    entities.append(practice_test)
    entities.append(practice_test_2)

    # reset_table_id_seq(session, PracticeTestEntity, PracticeTestEntity.resource_id, 1)

    session.commit()


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
    yield
