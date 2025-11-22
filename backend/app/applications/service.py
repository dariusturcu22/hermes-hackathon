from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func, desc
from typing import List, Optional, Tuple
from datetime import datetime

from backend.app.applications.model import Application
from backend.app.applications.schema import ApplicationCreate, ApplicationUpdate, ApplicationStatus
from backend.app.users.model import User
from backend.app.events.model import Opportunity
from backend.app.organizations.model import Organization


class ApplicationService:
    @staticmethod
    def get_application(db: Session, application_id: int) -> Optional[Application]:
        return db.query(Application).filter(Application.id == application_id).first()

    @staticmethod
    def get_applications(
            db: Session,
            skip: int = 0,
            limit: int = 100,
            user_id: Optional[int] = None,
            opportunity_id: Optional[int] = None,
            status: Optional[str] = None
    ) -> List[Application]:
        query = db.query(Application)

        if user_id:
            query = query.filter(Application.user_id == user_id)

        if opportunity_id:
            query = query.filter(Application.opportunity_id == opportunity_id)

        if status:
            query = query.filter(Application.status == status)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_applications_with_details(
            db: Session,
            skip: int = 0,
            limit: int = 100,
            user_id: Optional[int] = None,
            opportunity_id: Optional[int] = None,
            organization_id: Optional[int] = None,
            status: Optional[str] = None
    ) -> List:
        query = db.query(
            Application,
            User.name.label('user_name'),
            User.email.label('user_email'),
            Opportunity.title.label('opportunity_title'),
            Organization.name.label('organization_name'),
            Opportunity.final_points.label('opportunity_final_points')
        ).join(
            User, Application.user_id == User.id
        ).join(
            Opportunity, Application.opportunity_id == Opportunity.id
        ).join(
            Organization, Opportunity.organization_id == Organization.id
        )

        if user_id:
            query = query.filter(Application.user_id == user_id)

        if opportunity_id:
            query = query.filter(Application.opportunity_id == opportunity_id)

        if organization_id:
            query = query.filter(Organization.id == organization_id)

        if status:
            query = query.filter(Application.status == status)

        results = query.order_by(desc(Application.applied_at)).offset(skip).limit(limit).all()

        # Convert to list of dictionaries for easier serialization
        applications_with_details = []
        for application, user_name, user_email, opp_title, org_name, final_points in results:
            application_dict = {**application.__dict__}
            application_dict['user_name'] = user_name
            application_dict['user_email'] = user_email
            application_dict['opportunity_title'] = opp_title
            application_dict['organization_name'] = org_name
            application_dict['opportunity_final_points'] = final_points
            applications_with_details.append(application_dict)

        return applications_with_details

    @staticmethod
    def create_application(db: Session, application: ApplicationCreate) -> Optional[Application]:
        # Check if application already exists
        existing_application = db.query(Application).filter(
            and_(
                Application.user_id == application.user_id,
                Application.opportunity_id == application.opportunity_id
            )
        ).first()

        if existing_application:
            return None  # Application already exists

        db_application = Application(**application.dict())

        db.add(db_application)
        db.commit()
        db.refresh(db_application)
        return db_application

    @staticmethod
    def update_application_status(
            db: Session,
            application_id: int,
            status: ApplicationStatus
    ) -> Optional[Application]:
        db_application = db.query(Application).filter(Application.id == application_id).first()

        if not db_application:
            return None

        db_application.status = status
        db_application.updated_at = datetime.now()
        db.commit()
        db.refresh(db_application)
        return db_application

    @staticmethod
    def delete_application(db: Session, application_id: int) -> bool:
        db_application = db.query(Application).filter(Application.id == application_id).first()

        if not db_application:
            return False

        db.delete(db_application)
        db.commit()
        return True

    @staticmethod
    def accept_application(db: Session, application_id: int) -> Optional[Application]:
        return ApplicationService.update_application_status(
            db, application_id, ApplicationStatus.ACCEPTED
        )

    @staticmethod
    def reject_application(db: Session, application_id: int) -> Optional[Application]:
        return ApplicationService.update_application_status(
            db, application_id, ApplicationStatus.REJECTED
        )

    @staticmethod
    def complete_application(db: Session, application_id: int) -> Optional[Application]:
        db_application = ApplicationService.update_application_status(
            db, application_id, ApplicationStatus.COMPLETED
        )

        if db_application:
            # Here you would also award points to the user
            # This would integrate with your points system
            pass

        return db_application

    @staticmethod
    def mark_no_show(db: Session, application_id: int) -> Optional[Application]:
        return ApplicationService.update_application_status(
            db, application_id, ApplicationStatus.NO_SHOW
        )

    @staticmethod
    def get_application_stats(db: Session, user_id: Optional[int] = None) -> dict:
        base_query = db.query(Application.status, func.count(Application.id))

        if user_id:
            base_query = base_query.filter(Application.user_id == user_id)

        status_counts = base_query.group_by(Application.status).all()

        stats = {status: count for status, count in status_counts}

        # Add total applications
        total_query = db.query(func.count(Application.id))
        if user_id:
            total_query = total_query.filter(Application.user_id == user_id)

        stats['total'] = total_query.scalar()

        return stats

    @staticmethod
    def get_opportunity_applications_count(db: Session, opportunity_id: int) -> Tuple[int, int]:
        """Get total and accepted applications count for an opportunity"""
        total = db.query(func.count(Application.id)).filter(
            Application.opportunity_id == opportunity_id
        ).scalar()

        accepted = db.query(func.count(Application.id)).filter(
            and_(
                Application.opportunity_id == opportunity_id,
                Application.status == ApplicationStatus.ACCEPTED
            )
        ).scalar()

        return total, accepted

    @staticmethod
    def can_apply_to_opportunity(db: Session, user_id: int, opportunity_id: int) -> bool:
        """Check if user can apply to an opportunity"""
        # Check if already applied
        existing = db.query(Application).filter(
            and_(
                Application.user_id == user_id,
                Application.opportunity_id == opportunity_id
            )
        ).first()

        if existing:
            return False

        # Check if opportunity is open and not full
        opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
        if not opportunity or opportunity.status != "open":
            return False

        if opportunity.max_participants:
            total_accepted = db.query(func.count(Application.id)).filter(
                and_(
                    Application.opportunity_id == opportunity_id,
                    Application.status.in_([ApplicationStatus.ACCEPTED, ApplicationStatus.PENDING])
                )
            ).scalar()

            if total_accepted >= opportunity.max_participants:
                return False

        return True