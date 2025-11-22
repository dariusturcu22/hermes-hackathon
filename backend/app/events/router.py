from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from backend.app.database import get_db
from backend.app.events.service import OpportunityService
from backend.app.events.schema import (
    OpportunityCreate,
    OpportunityUpdate,
    OpportunityInDB,
    OpportunityResponse,
    OpportunityListResponse,
    OpportunityStatus
)

router = APIRouter()


@router.get("/opportunities", response_model=OpportunityListResponse)
def get_opportunities(
        skip: int = 0,
        limit: int = 100,
        organization_id: Optional[int] = Query(None),
        status: Optional[OpportunityStatus] = Query(None),
        difficulty: Optional[str] = Query(None),
        db: Session = Depends(get_db)
):
    """Get all opportunities with optional filtering"""
    opportunities = OpportunityService.get_opportunities_with_organization(
        db, skip=skip, limit=limit, status=status
    )

    return {
        "success": True,
        "data": opportunities,
        "total": len(opportunities)
    }


@router.get("/opportunities/{opportunity_id}", response_model=OpportunityResponse)
def get_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    """Get a specific opportunity by ID"""
    opportunity = OpportunityService.get_opportunity(db, opportunity_id)

    if not opportunity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity not found"
        )

    return {
        "success": True,
        "data": opportunity
    }


@router.post("/opportunities", response_model=OpportunityResponse, status_code=status.HTTP_201_CREATED)
def create_opportunity(opportunity: OpportunityCreate, db: Session = Depends(get_db)):
    """Create a new opportunity"""
    db_opportunity = OpportunityService.create_opportunity(db, opportunity)

    return {
        "success": True,
        "data": db_opportunity
    }


@router.put("/opportunities/{opportunity_id}", response_model=OpportunityResponse)
def update_opportunity(
        opportunity_id: int,
        opportunity_update: OpportunityUpdate,
        db: Session = Depends(get_db)
):
    """Update an existing opportunity"""
    db_opportunity = OpportunityService.update_opportunity(db, opportunity_id, opportunity_update)

    if not db_opportunity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity not found"
        )

    return {
        "success": True,
        "data": db_opportunity
    }


@router.delete("/opportunities/{opportunity_id}")
def delete_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    """Delete an opportunity"""
    success = OpportunityService.delete_opportunity(db, opportunity_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity not found"
        )

    return {
        "success": True,
        "message": "Opportunity deleted successfully"
    }


@router.post("/opportunities/{opportunity_id}/close", response_model=OpportunityResponse)
def close_opportunity(opportunity_id: int, db: Session = Depends(get_db)):
    """Close an opportunity (stop accepting applications)"""
    db_opportunity = OpportunityService.close_opportunity(db, opportunity_id)

    if not db_opportunity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Opportunity not found"
        )

    return {
        "success": True,
        "data": db_opportunity
    }


@router.get("/opportunities/upcoming")
def get_upcoming_opportunities(
        limit: int = Query(10, le=50),
        db: Session = Depends(get_db)
):
    """Get upcoming open opportunities"""
    opportunities = OpportunityService.get_upcoming_opportunities(db, limit)

    return {
        "success": True,
        "data": opportunities
    }


@router.get("/stats/opportunities")
def get_opportunity_stats(db: Session = Depends(get_db)):
    """Get statistics about opportunities"""
    stats = OpportunityService.count_opportunities_by_status(db)

    return {
        "success": True,
        "data": stats
    }