from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.analysis import AnalysisDetailResponse, AnalysisHistoryItem
from app.services.history_service import get_analysis_by_id, get_analysis_history, delete_analysis_by_id

router = APIRouter(prefix="/history", tags=["History"])

@router.get("", response_model=list[AnalysisHistoryItem])
def list_analysis_history(
    db: Session = Depends(get_db),
)-> list[AnalysisHistoryItem]:
    return get_analysis_history(db)

@router.get("/{analysis_id}", response_model=AnalysisDetailResponse)
def get_analysis_detail(
    analysis_id: int,
    db: Session = Depends(get_db),
) -> AnalysisDetailResponse:
    analysis = get_analysis_by_id(db, analysis_id)

    if analysis is None:
        raise HTTPException(
            status_code=404,
            detail=f"Analysis with id {analysis_id} not found",
        )

    return analysis

@router.delete("/{analysis_id}")
def delete_analysis(
    analysis_id: int,
    db: Session = Depends(get_db),
) -> dict:
    deleted = delete_analysis_by_id(db, analysis_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail=f"Analysis with id {analysis_id} not found",
        )

    return {
        "message": f"Analysis with id {analysis_id} deleted successfully"
    }