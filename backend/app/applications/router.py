from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from .service import ApplicationService
from .schema import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
    ApplicationWithDetailsResponse,
    ApplicationListResponse,
    ApplicationStatsResponse,
    ApplicationStatus
)

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.get("/applications", response_model=ApplicationListResponse)
def get_applications(
        skip: int = 0,
        limit: int = 100,
        user_id: Optional[int] = Query(None),
        event_id: Optional[int] = Query(None),
        organization_id: Optional[int] = Query(None),
        status: Optional[ApplicationStatus] = Query(None),
        db: Session = Depends(get_db)
):
    """Get all applications with details"""
    applications = ApplicationService.get_applications_with_details(
        db, skip=skip, limit=limit,
        user_id=user_id, event_id=event_id,
        organization_id=organization_id, status=status
    )
    return {"success": True, "data": applications, "total": len(applications)}


@router.get("/applications/{application_id}", response_model=ApplicationWithDetailsResponse)
def get_application(application_id: int, db: Session = Depends(get_db)):
    apps = ApplicationService.get_applications_with_details(
        db, limit=1, application_id=application_id
    )
    if not apps:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"success": True, "data": apps[0]}


@router.post("/applications", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(application: ApplicationCreate, db: Session = Depends(get_db)):
    if not ApplicationService.can_apply_to_event(db, application.user_id, application.event_id):
        raise HTTPException(
            status_code=400,
            detail="Cannot apply to this event (already applied, closed, or full)."
        )
    db_app = ApplicationService.create_application(db, application)
    if not db_app:
        raise HTTPException(status_code=400, detail="User or event does not exist")
    return {"success": True, "data": db_app}


@router.put("/applications/{application_id}", response_model=ApplicationResponse)
def update_application_status(application_id: int, application_update: ApplicationUpdate,
                              db: Session = Depends(get_db)):
    if not application_update.status:
        raise HTTPException(status_code=400, detail="Status is required")
    db_app = ApplicationService.update_application_status(db, application_id, application_update.status)
    if not db_app:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"success": True, "data": db_app}


@router.post("/applications/{application_id}/accept", response_model=ApplicationResponse)
def accept_application(application_id: int, db: Session = Depends(get_db)):
    db_app = ApplicationService.accept_application(db, application_id)
    if not db_app:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"success": True, "data": db_app}


@router.post("/applications/{application_id}/reject", response_model=ApplicationResponse)
def reject_application(application_id: int, db: Session = Depends(get_db)):
    db_app = ApplicationService.reject_application(db, application_id)
    if not db_app:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"success": True, "data": db_app}


@router.post("/applications/{application_id}/complete", response_model=ApplicationResponse)
def complete_application(application_id: int, db: Session = Depends(get_db)):
    db_app = ApplicationService.complete_application(db, application_id)
    if not db_app:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"success": True, "data": db_app}


@router.post("/applications/{application_id}/no-show", response_model=ApplicationResponse)
def mark_no_show(application_id: int, db: Session = Depends(get_db)):
    db_app = ApplicationService.mark_no_show(db, application_id)
    if not db_app:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"success": True, "data": db_app}


@router.delete("/applications/{application_id}")
def delete_application(application_id: int, db: Session = Depends(get_db)):
    success = ApplicationService.delete_application(db, application_id)
    if not success:
        raise HTTPException(status_code=404, detail="Application not found")
    return {"success": True, "message": "Application deleted successfully"}


@router.get("/stats/applications", response_model=ApplicationStatsResponse)
def get_application_stats(user_id: Optional[int] = Query(None), db: Session = Depends(get_db)):
    stats = ApplicationService.get_application_stats(db, user_id)
    return {"success": True, "data": stats}


@router.get("/opportunities/{event_id}/applications/count")
def get_event_applications_count(event_id: int, db: Session = Depends(get_db)):
    total, accepted = ApplicationService.get_event_applications_count(db, event_id)
    return {"success": True,
            "data": {"event_id": event_id, "total_applications": total, "accepted_applications": accepted}}


@router.get("/applications/check-eligibility")
def check_application_eligibility(user_id: str = Query(...), event_id: str = Query(...), db: Session = Depends(get_db)):
    print(user_id, event_id)
    can_apply = ApplicationService.can_apply_to_event(db, user_id, event_id)
    return {"success": True, "data": {"user_id": user_id, "event_id": event_id, "can_apply": can_apply}}
