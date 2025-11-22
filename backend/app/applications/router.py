from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from ..database import get_db
from .service import ApplicationService
from .schema import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationResponse,
    ApplicationWithDetailsResponse,
    ApplicationListResponse,
    ApplicationStatsResponse,
    ApplicationStatus, ResponseWrapper
)

router = APIRouter()


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
    """Get all applications with detailed information"""
    applications = ApplicationService.get_applications_with_details(
        db, skip=skip, limit=limit, user_id=user_id,
        event_id=event_id, organization_id=organization_id, status=status
    )

    return {
        "success": True,
        "data": applications,
        "total": len(applications)
    }


@router.get("/applications/{application_id}", response_model=ResponseWrapper)
def get_application(application_id: int, db: Session = Depends(get_db)):
    """Get a specific application by ID with details"""
    applications = ApplicationService.get_applications_with_details(
        db, limit=1, application_id=application_id
    )

    if not applications or applications[0] is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    return {
        "success": True,
        "data": applications[0]
    }


@router.post("/applications", response_model=ApplicationResponse, status_code=status.HTTP_201_CREATED)
def create_application(application: ApplicationCreate, db: Session = Depends(get_db)):
    """Create a new application (volunteer applies to event)"""
    # Check if user can apply to this event
    if not ApplicationService.can_apply_to_event(
            db, application.user_id, application.event_id
    ):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot apply to this event. Already applied, event closed, or full."
        )

    db_application = ApplicationService.create_application(db, application)

    if not db_application:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Application already exists"
        )

    return {
        "success": True,
        "data": db_application
    }


@router.put("/applications/{application_id}", response_model=ApplicationResponse)
def update_application_status(
        application_id: int,
        application_update: ApplicationUpdate,
        db: Session = Depends(get_db)
):
    """Update application status"""
    if not application_update.status:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Status is required for update"
        )

    db_application = ApplicationService.update_application_status(
        db, application_id, application_update.status
    )

    if not db_application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    return {
        "success": True,
        "data": db_application
    }


@router.post("/applications/{application_id}/accept", response_model=ApplicationResponse)
def accept_application(application_id: int, db: Session = Depends(get_db)):
    """Accept an application"""
    db_application = ApplicationService.accept_application(db, application_id)

    if not db_application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    return {
        "success": True,
        "data": db_application
    }


@router.post("/applications/{application_id}/reject", response_model=ApplicationResponse)
def reject_application(application_id: int, db: Session = Depends(get_db)):
    """Reject an application"""
    db_application = ApplicationService.reject_application(db, application_id)

    if not db_application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    return {
        "success": True,
        "data": db_application
    }


@router.post("/applications/{application_id}/complete", response_model=ApplicationResponse)
def complete_application(application_id: int, db: Session = Depends(get_db)):
    """Mark application as completed (volunteer attended)"""
    db_application = ApplicationService.complete_application(db, application_id)

    if not db_application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    return {
        "success": True,
        "data": db_application
    }


@router.post("/applications/{application_id}/no-show", response_model=ApplicationResponse)
def mark_no_show(application_id: int, db: Session = Depends(get_db)):
    """Mark application as no-show (volunteer didn't attend)"""
    db_application = ApplicationService.mark_no_show(db, application_id)

    if not db_application:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    return {
        "success": True,
        "data": db_application
    }


@router.delete("/applications/{application_id}")
def delete_application(application_id: int, db: Session = Depends(get_db)):
    """Delete an application"""
    success = ApplicationService.delete_application(db, application_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Application not found"
        )

    return {
        "success": True,
        "message": "Application deleted successfully"
    }


@router.get("/stats/applications")
def get_application_stats(
        user_id: Optional[int] = Query(None),
        db: Session = Depends(get_db)
):
    """Get application statistics"""
    stats = ApplicationService.get_application_stats(db, user_id)

    return {
        "success": True,
        "data": stats
    }


@router.get("/opportunities/{event_id}/applications/count")
def get_event_applications_count(event_id: int, db: Session = Depends(get_db)):
    """Get application counts for an event"""
    total, accepted = ApplicationService.get_event_applications_count(db, event_id)

    return {
        "success": True,
        "data": {
            "event_id": event_id,
            "total_applications": total,
            "accepted_applications": accepted
        }
    }


@router.get("/applications/check-eligibility")
def check_application_eligibility(
        user_id: int = Query(...),
        event_id: int = Query(...),
        db: Session = Depends(get_db)
):
    """Check if a user can apply to an event"""
    can_apply = ApplicationService.can_apply_to_event(db, user_id, event_id)

    return {
        "success": True,
        "data": {
            "user_id": user_id,
            "event_id": event_id,
            "can_apply": can_apply
        }
    }
