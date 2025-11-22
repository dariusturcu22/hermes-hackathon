from sqlalchemy.orm import Session
from sqlalchemy import and_, func, desc
from typing import List, Optional, Tuple
from datetime import datetime

from ..applications.model import Application
from ..applications.schema import ApplicationCreate, ApplicationStatus
from ..users.model import User
from ..events.model import Event
from ..organizations.model import Organization


class ApplicationService:
    @staticmethod
    def get_application(db: Session, application_id: int) -> Optional[Application]:
        return db.query(Application).filter(Application.id == application_id).first()

    @staticmethod
    def get_applications_with_details(
            db: Session,
            skip: int = 0,
            limit: int = 100,
            user_id: Optional[int] = None,
            event_id: Optional[int] = None,
            application_id: Optional[int] = None,
            organization_id: Optional[int] = None,
            status: Optional[ApplicationStatus] = None
    ) -> List:
        query = db.query(
            Application,
            User.name.label("user_name"),
            User.email.label("user_email"),
            Event.title.label("event_title"),
            Organization.name.label("organization_name"),
            Event.final_points.label("event_final_points")
        ).join(User).join(Event).join(Organization)

        if user_id:
            query = query.filter(Application.user_id == user_id)
        if event_id:
            query = query.filter(Application.event_id == event_id)
        if application_id:
            query = query.filter(Application.id == application_id)
        if organization_id:
            query = query.filter(Organization.id == organization_id)
        if status:
            query = query.filter(Application.status == status)

        results = query.order_by(desc(Application.applied_at)).offset(skip).limit(limit).all()

        apps = []
        for application, user_name, user_email, event_title, org_name, final_points in results:
            app_dict = {
                **application.__dict__,
                "user_name": user_name,
                "user_email": user_email,
                "event_title": event_title,
                "organization_name": org_name,
                "event_final_points": final_points
            }
            apps.append(app_dict)

        return apps

    @staticmethod
    def create_application(db: Session, application: ApplicationCreate) -> Optional[Application]:
        # Check user exists
        user = db.query(User).filter(User.id == application.user_id).first()
        if not user:
            return None

        # Check event exists
        event = db.query(Event).filter(Event.id == application.event_id).first()
        if not event:
            return None

        # Check if application exists
        existing = db.query(Application).filter(
            and_(
                Application.user_id == application.user_id,
                Application.event_id == application.event_id
            )
        ).first()
        if existing:
            return None

        db_app = Application(
            user_id=application.user_id,
            event_id=application.event_id,
            status=ApplicationStatus.PENDING
        )
        db.add(db_app)
        db.commit()
        db.refresh(db_app)
        return db_app

    @staticmethod
    def update_application_status(db: Session, application_id: int, status: ApplicationStatus) -> Optional[Application]:
        app = db.query(Application).filter(Application.id == application_id).first()
        if not app:
            return None
        app.status = status
        app.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(app)
        return app

    @staticmethod
    def delete_application(db: Session, application_id: int) -> bool:
        app = db.query(Application).filter(Application.id == application_id).first()
        if not app:
            return False
        db.delete(app)
        db.commit()
        return True

    @staticmethod
    def accept_application(db: Session, application_id: int) -> Optional[Application]:
        return ApplicationService.update_application_status(db, application_id, ApplicationStatus.ACCEPTED)

    @staticmethod
    def reject_application(db: Session, application_id: int) -> Optional[Application]:
        return ApplicationService.update_application_status(db, application_id, ApplicationStatus.REJECTED)

    @staticmethod
    def complete_application(db: Session, application_id: int) -> Optional[Application]:
        return ApplicationService.update_application_status(db, application_id, ApplicationStatus.COMPLETED)

    @staticmethod
    def mark_no_show(db: Session, application_id: int) -> Optional[Application]:
        return ApplicationService.update_application_status(db, application_id, ApplicationStatus.NO_SHOW)

    @staticmethod
    def get_application_stats(db: Session, user_id: Optional[int] = None) -> dict:
        query = db.query(Application.status, func.count(Application.id))
        if user_id:
            query = query.filter(Application.user_id == user_id)
        counts = query.group_by(Application.status).all()
        stats = {status: count for status, count in counts}
        total = db.query(func.count(Application.id))
        if user_id:
            total = total.filter(Application.user_id == user_id)
        stats["total"] = total.scalar()
        return stats

    @staticmethod
    def get_event_applications_count(db: Session, event_id: int) -> Tuple[int, int]:
        total = db.query(func.count(Application.id)).filter(Application.event_id == event_id).scalar()
        accepted = db.query(func.count(Application.id)).filter(
            and_(Application.event_id == event_id, Application.status == ApplicationStatus.ACCEPTED)
        ).scalar()
        return total, accepted

    @staticmethod
    def can_apply_to_event(db: Session, user_id: int, event_id: int) -> bool:
        # Check user exists
        if not db.query(User).filter(User.id == user_id).first():
            return False

        # Check event exists and is open
        event = db.query(Event).filter(Event.id == event_id).first()
        if not event or event.status != "open":
            return False

        # Check if already applied
        if db.query(Application).filter(
                and_(Application.user_id == user_id, Application.event_id == event_id)
        ).first():
            return False

        # Check max participants
        if event.max_participants:
            total_accepted = db.query(func.count(Application.id)).filter(
                and_(
                    Application.event_id == event_id,
                    Application.status.in_([ApplicationStatus.ACCEPTED, ApplicationStatus.PENDING])
                )
            ).scalar()
            if total_accepted >= event.max_participants:
                return False

        return True
