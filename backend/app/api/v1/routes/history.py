from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.analysis import AnalysisDetailResponse, AnalysisHistoryItem
from app.services.history_service import get_analysis_by_id, get_analysis_history

router = APIRouter(prefix="/history", tags=["History"])

@router.get("", response_model=list[AnalysisHistoryItem])
def list_analysis_history(
    db: Session = Depends(get_db),
)-> list[AnalysisHistoryItem]:
    return get_analysis_history(db)

