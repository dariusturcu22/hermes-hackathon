from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from . import service
from .schema import PointsHistoryCreate, PointsHistoryRead, PointsHistoryUpdate

router = APIRouter(prefix="/points_history", tags=["Points History"])


@router.post("/", response_model=PointsHistoryRead, status_code=status.HTTP_201_CREATED)
def create_points_history(data: PointsHistoryCreate, db: Session = Depends(get_db)):
    return service.create_points_history(db, data)


@router.get("/", response_model=list[PointsHistoryRead])
def get_points_history(db: Session = Depends(get_db)):
    return service.get_points_history(db)


@router.get("/{entry_id}", response_model=PointsHistoryRead)
def get_points_history_by_id(entry_id: int, db: Session = Depends(get_db)):
    entry = service.get_points_history_by_id(db, entry_id)
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Points history entry not found")

    return entry


@router.patch("/{entry_id}", response_model=PointsHistoryRead)
def update_points_history(entry_id: int, data: PointsHistoryUpdate, db: Session = Depends(get_db)):
    entry = service.update_points_history(db, entry_id, data)
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Points history entry not found")

    return entry


@router.delete("/{entry_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_points_history(entry_id: int, db: Session = Depends(get_db)):
    success = service.delete_points_history(db, entry_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Points history entry not found")

    return None
