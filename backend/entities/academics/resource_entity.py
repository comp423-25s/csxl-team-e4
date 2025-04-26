from typing import Self
from sqlalchemy import ForeignKey, Integer, LargeBinary, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.entities.academics.course_entity import CourseEntity
from ..entity_base import EntityBase
from ...models.academics import Course
from ...models.academics import CourseDetails
from ...models.academics.resource import Resource



class ResourceEntity(EntityBase):
    """Serves as the database model schema defining the shape of the `Resource` table"""

    # Name for the resource table in the PostgreSQL database
    __tablename__ = "academics__resource"

    # Resource properties (columns in the database table)

    # Unique ID for the resource
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ta_upload: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    file_data: Mapped[bytes] = mapped_column(LargeBinary, nullable=False)
    course_id: Mapped[str] = mapped_column(String, ForeignKey("academics__course.id"), nullable=False)
    course: Mapped["CourseEntity"] = relationship(back_populates="resources")

    # Not including file_data b/c that is a raw binary file
    def to_model(self) -> Resource:
        return Resource(
            id=self.id,
            title=self.title,
            file_name=self.file_name,
            ta_upload=self.ta_upload



        )