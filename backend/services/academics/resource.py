from backend.database import Session, db_session
from sqlalchemy.orm import Session as SQLAlchemySession
from sqlalchemy import select
from fastapi import Depends
from backend.entities.academics.course_entity import CourseEntity
from backend.entities.academics.resource_entity import ResourceEntity
from backend.models.academics.resource import Resource
from typing import Annotated, Optional


class ResourceService:
    _session: Session

    def __init__(
        self,
        session: Annotated[Session, Depends(db_session)]
    ):
        self._session = session

    def delete(self, resource_id: int) -> bool:
        query = select(ResourceEntity).filter(ResourceEntity.id == resource_id)
        entity = self._session.scalars(query).one_or_none()
        if entity is None:
            return False
        self._session.delete(entity)
        self._session.commit()
        return True

    def get_all_resources(self) -> list[Resource]:
        query = select(ResourceEntity)
        entities = self._session.scalars(query).all()
        return [entity.to_model() for entity in entities]
    
    def get_resource_by_id(self, resource_id: int) -> Optional[ResourceEntity]:
        query = select(ResourceEntity).filter(ResourceEntity.id == resource_id)
        return self._session.scalars(query).one_or_none()
    
    def get_resources_by_course_id(self, course_id: str) -> list[Resource]:
        course_entity_query = select(CourseEntity).filter(CourseEntity.pk == course_id)
        course_entity = self._session.scalars(course_entity_query).one_or_none()
        query = select(ResourceEntity).filter(ResourceEntity.course_id == course_entity.id)
        entities = self._session.scalars(query).all()
        return [entity.to_model() for entity in entities]

    def create_new_resource(self, title: str, file_name: str, course_id: str, file_blob: bytes):
        new_resource = ResourceEntity(
            title=title,
            file_name=file_name,
            course_id=course_id,
            file_data=file_blob
        )
        self._session.add(new_resource)
        self._session.commit()
        self._session.refresh(new_resource)
        return new_resource