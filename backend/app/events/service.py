from sqlalchemy.orm import Session
from sqlalchemy import func, and_
from typing import Optional, List
from datetime import datetime

from ..events.model import Event
from ..events.schema import EventCreate, EventUpdate, EventStatus, EventWithOrganization
from ..organizations.model import Organization


class EventService:

    @staticmethod
    def get_event(db: Session, event_id: int) -> Optional[Event]:
        return db.query(Event).filter(Event.id == event_id).first()

    @staticmethod
    def get_events_with_organization(
            db: Session,
            skip: int = 0,
            limit: int = 100,
            status: Optional[EventStatus] = None,
            organization_id: Optional[int] = None,
            difficulty: Optional[str] = None,
    ) -> List[EventWithOrganization]:
        query = db.query(Event, Organization.name.label("organization_name")) \
            .join(Organization, Event.organization_id == Organization.id)

        if status is not None:
            query = query.filter(Event.status == status.value)
        if organization_id is not None:
            query = query.filter(Event.organization_id == organization_id)
        if difficulty is not None:
            query = query.filter(Event.difficulty == difficulty)

        results = query.offset(skip).limit(limit).all()

        out: List[EventWithOrganization] = []
        for event, org_name in results:
            # build plain dict with only the public attributes
            d = {
                "id": event.id,
                "title": event.title,
                "description": event.description,
                "location": event.location,
                "date_start": event.date_start,
                "date_end": event.date_end,
                "difficulty": event.difficulty,
                "duration_minutes": event.duration_minutes,
                "proposed_points": event.proposed_points,
                "final_points": event.final_points,
                "max_participants": event.max_participants,
                "status": event.status,
                "organization_id": event.organization_id,
                "created_at": event.created_at,
                "updated_at": event.updated_at,
                "organization_name": org_name,
            }
            out.append(EventWithOrganization.parse_obj(d))
        return out

    @staticmethod
    def create_event(db: Session, data: EventCreate) -> Event:
        # ensure organization exists
        org = db.query(Organization).filter(Organization.id == data.organization_id).first()
        if not org:
            raise ValueError(f"Organization id={data.organization_id} does not exist")

        # explicit mapping to DB-friendly types (enums -> strings)
        payload = data.model_dump()
        payload["difficulty"] = data.difficulty
        payload["final_points"] = data.proposed_points
        payload["status"] = EventStatus.OPEN.value

        event = Event(**payload)
        db.add(event)
        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def update_event(db: Session, event_id: int, data: EventUpdate) -> Optional[Event]:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return None

        update_data = data.model_dump(exclude_unset=True)
        # normalize enums to values for DB
        for k, v in update_data.items():
            if isinstance(v, EventStatus):
                setattr(event, k, v.value)
            else:
                # if difficulty provided as Enum -> store string
                # Pydantic will supply Enum members for difficulty if used
                if k == "difficulty" and v is not None and hasattr(v, "value"):
                    setattr(event, k, v.value)
                else:
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
    def close_event(db: Session, event_id: int) -> Optional[Event]:
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event:
            return None
        event.status = EventStatus.CLOSED.value
        event.updated_at = datetime.now()
        db.commit()
        db.refresh(event)
        return event

    @staticmethod
    def upcoming_events(db: Session, limit: int = 10) -> List[Event]:
        return db.query(Event) \
            .filter(and_(Event.status == EventStatus.OPEN.value,
                         Event.date_start > datetime.now())) \
            .order_by(Event.date_start.asc()) \
            .limit(limit).all()

    @staticmethod
    def count_by_status(db: Session) -> dict:
        results = db.query(Event.status, func.count(Event.id)).group_by(Event.status).all()
        return {status: count for status, count in results}
