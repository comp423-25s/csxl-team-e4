from pydantic import BaseModel

class Resource(BaseModel):
    title: str
    file_name: str
