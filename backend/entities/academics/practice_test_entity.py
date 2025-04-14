from datetime import datetime
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Enum as SQLAlchemyEnum
from ..entity_base import EntityBase
from typing import Self
from ...models.academics.practice_test import AIResponse
from ...models.academics.practice_test import OpenAPIResponse


class PracticeTestEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `PracticeTest` table"""

    # Name for the practice test table in the PostgreSQL database
    __tablename__ = "practice_test"

    # Unique ID for the practice test (primary key)
    resource_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    # User associated with the test
    user: Mapped[str] = mapped_column(String, nullable=False)

    # Course associated with the practice test
    course: Mapped[str] = mapped_column(String, nullable=False)

    # The prompt provided by the user to generate the test
    user_prompt: Mapped[str] = mapped_column(Text, nullable=False)

    # The content of the practice test generated from AI
    test_contents: Mapped[str] = mapped_column(Text, nullable=False)

    # Time when the practice test was created (for tracking purposes)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=datetime.now
    )

    instructor_approved: Mapped[bool] = mapped_column(
        Boolean, nullable=False, default=False
    )

    # Method to convert from a draft or another model into an entity
    @classmethod
    def from_draft(
        cls,
        user: str,
        course: str,
        user_prompt: str,
        test_contents: str,
        created_at: datetime,
        instructor_approved: bool,
    ) -> Self:
        """Converts input data to a practice test entity"""
        return cls(
            user=user,
            course=course,
            user_prompt=user_prompt,
            test_contents=test_contents,
            created_at=created_at,
            instructor_approved=instructor_approved,
        )

    # Method to convert to a response model
    def to_response_model(self) -> AIResponse:
        """Converts the practice test entity to an AIResponse model"""
        return AIResponse(response_id=self.resource_id, test=self.test_contents)
