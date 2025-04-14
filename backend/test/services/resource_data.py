from backend.models.academics.resource import Resource
from ...entities.academics.resource_entity import ResourceEntity
from sqlalchemy.orm import Session
import os

resources = [
    Resource(title="Variables and Data Types", file_name="variables.pdf"),
    Resource(title="Conditionals and Booleans", file_name="conditionals.pdf"),
    Resource(title="Loops in Python", file_name="loops.pdf"),
    Resource(title="Functions in Python", file_name="functions.pdf"),
    Resource(title="Lists and Dictionaries", file_name="lists_and_dicts.pdf"),
    Resource(title="String Manipulation", file_name="strings.pdf"),
    Resource(title="Error Handling", file_name="error_handling.pdf"),
]

def insert_fake_resources(session: Session, pdf_dir: str = None, course_id: str = "comp110"):
    session.query(ResourceEntity).delete()
    pdf_dir = pdf_dir or "backend/sample-pdfs"
    for r in resources:
        full_path = os.path.join(pdf_dir, r.file_name)
        if not os.path.exists(full_path):
            print(f"Missing file: {r.file_name}")
            continue

        with open(full_path, "rb") as f:
            file_data = f.read()

        entity = ResourceEntity(
            title=r.title,
            file_name=r.file_name,
            file_data=file_data,
            course_id=course_id
        )
        session.add(entity)

    session.commit()
    print("Inserted resource data for COMP110.")