from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from backend.models.academics.resource import Resource
from backend.services.academics.resource import ResourceService
from fastapi.responses import StreamingResponse
import io

api = APIRouter(
    prefix="/api/academics/resources",
    tags=["Academics"]
)

@api.get("/", response_model=list[Resource])
def get_resources(
    svc: Annotated[ResourceService, Depends()]
):
    return svc.get_all_resources()

@api.delete("/{resource_id}")
def delete_resource(
    resource_id: int,
    svc: Annotated[ResourceService, Depends()]
):
    success = svc.delete(resource_id)
    if not success:
        raise HTTPException(status_code=404, detail="Resource not found")
    return {"message": "Resource deleted successfully"}

@api.get("/{resource_id}/download")
def download_resource(
    resource_id: int,
    svc: Annotated[ResourceService, Depends()]
):
    resource = svc.get_resource_by_id(resource_id)
    if resource is None:
        raise HTTPException(status_code=404, detail="Resource not found")

    return StreamingResponse(
        io.BytesIO(resource.file_data),
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename={resource.file_name}"}
    )
