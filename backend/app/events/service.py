from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Optional, List
from datetime import datetime

from ..events.model import Event
from ..events.schema import EventCreate, EventUpdate, EventStatus
from ..organizations.model import Organization


class EventService:
    @staticmethod
    def get_event(db: Session, event_id: int) -> Optional[Event]:
        return db.query(Event).filter(Event.id == event_id).first()

    @staticmethod
    def list_events(
            db: Session,
            skip: int = 0,
            limit: int = 100,
            organization_id: Optional[int] = None,
            status: Optional[EventStatus] = None,
            difficulty: Optional[str] = None,
    ) -> List[Event]:

        query = db.query(Event)

        if organization_id is not None:
            query = query.filter(Event.organization_id == organization_id)
        if status is not None:
            query = query.filter(Event.status == status)
        if difficulty is not None:
            query = query.filter(Event.difficulty == difficulty)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def list_events_with_organization(
            db: Session,
            skip: int = 0,
            limit: int = 100,
            status: Optional[EventStatus] = None,
    ):
        query = (
            db.query(Event, Organization.name.label("organization_name"))
            .join(Organization, Event.organization_id == Organization.id)
        )

        if status is not None:
            query = query.filter(Event.status == status)

        results = query.offset(skip).limit(limit).all()

        return [
            {
                **event.__dict__,
                "organization_name": org_name,
            }
            for event, org_name in results
        ]

    @staticmethod
    def create_event(db: Session, data: EventCreate) -> Event:
        final_points = data.proposed_points

        event = Event(
            **data.model_dump(),
            final_points=final_points,
            status=EventStatus.OPEN,
        )

        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def update_event(db: Session, event_id: int, data: EventUpdate):
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for k, v in update_data.items():
            setattr(event, k, v)

        event.updated_at = datetime.now()
        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def delete_event(db: Session, event_id: int) -> bool:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return False

        db.delete(event)
        db.commit()
        return True

    @staticmethod
    def close_event(db: Session, event_id: int):
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return None

        event.status = EventStatus.CLOSED
        event.updated_at = datetime.now()
        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def upcoming_events(db: Session, limit: int = 10):
        return (
            db.query(Event)
            .filter(
                and_(
                    Event.status == EventStatus.OPEN,
                    Event.date_start > datetime.now(),
                )
            )
            .order_by(Event.date_start.asc())
            .limit(limit)
            .all()
        )

    @staticmethod
    def count_by_status(db: Session) -> dict:
        results = db.query(Event.status, func.count(Event.id)).group_by(Event.status).all()
        return {status: count for status, count in results}
