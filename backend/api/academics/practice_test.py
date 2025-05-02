from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Response
from backend.models.academics.practice_test import AIResponse, AIRequest, LatexRequest
from backend.services.academics.practice_test import PracticeTestService
import os
import subprocess
import tempfile
from fastapi.responses import FileResponse
from fastapi import Body
from html import unescape

api = APIRouter(
    prefix="/api/academics/practice_test",
    tags=["Academics"]
)


@api.get(
    "/retrieve_response/{response_id}", tags=["Academics"], response_model=AIResponse
)
def get_response(response_id: int, svc: Annotated[PracticeTestService, Depends()]):
    response = svc.get_response(response_id)
    if response is None:
        raise HTTPException(status_code=404, detail="Response not found")
    return response


@api.post("/generate_test", tags=["Academics"], response_model=AIResponse)
def generate_test(req: AIRequest, svc: Annotated[PracticeTestService, Depends()]):
    return svc.generate_test(req)


@api.delete("/delete_response/{response_id}", tags=["Academics"])
def delete_response(response_id: int, svc: Annotated[PracticeTestService, Depends()]):
    success = svc.delete_response(response_id)
    if not success:
        raise HTTPException(status_code=404, detail="Response not found")
    return f"Response {response_id} deleted successfully"



@api.get("/generate_pdf/{resource_id}", tags=["Academics"])
def generate_pdf_from_db(
    resource_id: int, svc: Annotated[PracticeTestService, Depends()]
):
    # Get the test via your service
    test = svc.get_response(resource_id)
    if not test or not test.test_contents:
        raise HTTPException(status_code=404, detail="LaTeX content not found")

    latex_str = svc.sanitize_latex(test.test_contents)

    with tempfile.TemporaryDirectory() as tmpdir:
        tex_path = os.path.join(tmpdir, "document.tex")
        pdf_path = os.path.join(tmpdir, "document.pdf")

        with open(tex_path, "w") as f:
            f.write(latex_str)

        result = subprocess.run(
            [
                "pdflatex",
                "-interaction=nonstopmode",
                "-output-directory",
                tmpdir,
                tex_path,
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        if result.returncode != 0 or not os.path.exists(pdf_path):
            print("======== STDOUT ========")
            print(result.stdout.decode())
            print("======== STDERR ========")
            print(result.stderr.decode())
            print("======== LATEX SOURCE ========")
            print(latex_str)
            raise HTTPException(status_code=500, detail="PDF generation failed")

        with open(pdf_path, "rb") as f:
            pdf_bytes = f.read()

        return Response(content=pdf_bytes, media_type="application/pdf")
