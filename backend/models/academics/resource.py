from pydantic import BaseModel
from typing import Optional


class Resource(BaseModel):
    id: Optional[int] = None
    title: str
    file_name: str
