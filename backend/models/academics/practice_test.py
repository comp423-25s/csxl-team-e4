from pydantic import BaseModel
from typing import List, Optional
from fastapi import UploadFile
from datetime import datetime


class AIRequest(BaseModel):
    """Requires user to input text to make a request, also allows them to upload a image or file"""

    text: str
    image: Optional[UploadFile] = None
    file: Optional[UploadFile] = None


class AIResponse(BaseModel):
    """Outputs the test as a string"""

    response_id: int
    test: str
    user: str
    course: str
    user_prompt: str
    test_contents: str
    created_at: datetime = datetime.now()
    instructor_approved: bool = False


class OpenAPIResponse(BaseModel):
    test: str
