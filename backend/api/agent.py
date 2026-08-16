from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.agent import AutomotiveDefectAgent
from backend.services.report import generate_report


router = APIRouter(
    prefix="/agent",
    tags=["AI Quality Agent"]
)


class DefectRequest(BaseModel):
    defect: str
    confidence: float


@router.post("/analyze")
def analyze(
    request: DefectRequest
):
    try:

        agent = AutomotiveDefectAgent()

        result = agent.analyze(
            defect=request.defect,
            confidence=request.confidence
        )

        return result

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


class ReportRequest(BaseModel):
    title: str
    analysis: str


@router.post("/report")
def report(
    request: ReportRequest
):

    path = generate_report(
        filename="inspection_report.pdf",
        title=request.title,
        analysis=request.analysis
    )

    return {
        "success": True,
        "file": path
    }