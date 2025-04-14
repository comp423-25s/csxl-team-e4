from pydantic import BaseModel
from typing import List, Optional
from fastapi import UploadFile


class AIRequest(BaseModel):
    """Requires user to input text to make a request, also allows them to upload a image or file"""

    text: str
    image: Optional[UploadFile] = None
    file: Optional[UploadFile] = None


class AIResponse(BaseModel):
    """Outputs the test as a string"""

    response_id: int
    test: str
    prompt: str
    topics: List[str]
    format: str
