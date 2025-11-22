from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import Optional

from ..database import get_db
from ..events.service import EventService
from ..events.schema import (
    EventCreate,
    EventUpdate,
    EventInDB,
    EventOut,
    EventListOut,
    EventStatus
)

router = APIRouter(prefix="/events", tags=["Events"])


@router.get("/", response_model=EventListOut)
def get_events(
        skip: int = 0,
        limit: int = 100,
        organization_id: Optional[int] = None,
        status: Optional[EventStatus] = None,
        difficulty: Optional[str] = None,
        db: Session = Depends(get_db),
):
    items = EventService.get_events_with_organization(
        db,
        skip=skip,
        limit=limit,
        status=status,
    )

    return {
        "success": True,
        "data": items,
        "total": len(items),
    }


@router.get("/{event_id}", response_model=EventOut)
def get_event(event_id: int, db: Session = Depends(get_db)):
    item = EventService.get_event(db, event_id)
    if not item:
        raise HTTPException(status_code=404, detail="Event not found")

    return {"success": True, "data": item}


@router.post("/", response_model=EventOut, status_code=201)
def create_event(data: EventCreate, db: Session = Depends(get_db)):
    item = EventService.create_event(db, data)
    return {"success": True, "data": item}


@router.put("/{event_id}", response_model=EventOut)
def update_event(event_id: int, data: EventUpdate, db: Session = Depends(get_db)):
    item = EventService.update_event(db, event_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="Event not found")

    return {"success": True, "data": item}


@router.delete("/{event_id}", response_model=dict)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    success = EventService.delete_event(db, event_id)
    if not success:
        raise HTTPException(status_code=404, detail="Event not found")

    return {"success": True, "message": "Event deleted successfully"}


@router.post("/{event_id}/close", response_model=EventOut)
def close_event(event_id: int, db: Session = Depends(get_db)):
    item = EventService.close_event(db, event_id)
    if not item:
        raise HTTPException(status_code=404, detail="Event not found")

    return {"success": True, "data": item}


@router.get("/upcoming", response_model=EventListOut)
def upcoming_events(limit: int = Query(10, le=50), db: Session = Depends(get_db)):
    items = EventService.get_upcoming_events(db, limit)
    return {"success": True, "data": items, "total": len(items)}


@router.get("/stats", response_model=dict)
def event_stats(db: Session = Depends(get_db)):
    stats = EventService.count_events_by_status(db)
    return {"success": True, "data": stats}
