from backend.models.academics.resource import Resource
from ...entities.academics.resource_entity import ResourceEntity
from sqlalchemy.orm import Session
import os

resources = [
    Resource(title="Variables and Data Types", file_name="variables.pdf", ta_upload=False),
    Resource(title="Conditionals and Booleans", file_name="conditionals.pdf", ta_upload=False),
    Resource(title="Loops in Python", file_name="loops.pdf", ta_upload=False),
    Resource(title="Functions in Python", file_name="functions.pdf", ta_upload=False),
    Resource(title="Lists and Dictionaries", file_name="lists_and_dicts.pdf", ta_upload=False),
    Resource(title="String Manipulation", file_name="strings.pdf", ta_upload=False),
    Resource(title="Error Handling", file_name="error_handling.pdf", ta_upload=True),
]

def insert_fake_resources(session: Session, pdf_dir: str = None, course_id: str = "comp110"):
    session.query(ResourceEntity).delete()
    pdf_dir = pdf_dir or "backend/sample-pdfs"
    ta = False
    for index, r in enumerate(resources):
        # Check if the current resource is the last one in the list
        if index == len(resources) - 1:
            course_id = "comp210"
            ta = True

        full_path = os.path.join(pdf_dir, r.file_name)
        if not os.path.exists(full_path):
            print(f"Missing file: {r.file_name}")
            continue

        with open(full_path, "rb") as f:
            file_data = f.read()

        entity = ResourceEntity(
            title=r.title,
            ta_upload=ta,
            file_name=r.file_name,
            file_data=file_data,
            course_id=course_id
        )
        session.add(entity)

    session.commit()
    print(f"Inserted resource data for {course_id}.")
