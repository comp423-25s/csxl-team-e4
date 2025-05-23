from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class AIRequest(BaseModel):
    """Requires user to input text to make a request, also allows them to upload a image or file"""

    prompt: str
    formats: List[str]
    resource_ids: List[int]


class AIResponse(BaseModel):
    """Outputs the test as a string"""

    response_id: int
    user: str
    course: str
    requested_prompt: Optional[str] = None
    user_prompt: str
    test_contents: str
    resources: Optional[List[str]] = None
    created_at: datetime = datetime.now()
    instructor_approved: bool = False


class LatexRequest(BaseModel):
    latex_str: str


class OpenAPIResponse(BaseModel):
    test: str
