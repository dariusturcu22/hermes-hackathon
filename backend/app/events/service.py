from alembic.operations.toimpl import drop_table
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func
from typing import List, Optional
from datetime import datetime
from backend.app.events.model import Opportunity
from backend.app.events.schema import OpportunityCreate, OpportunityUpdate, OpportunityStatus
from backend.app.organizations.model import Organization

class OpportunityService:
    @staticmethod
    def get_opportunity(db: Session, opportunity_id: int) -> Optional[Opportunity]:
        return db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()

    @staticmethod
    def get_opportunities(
            db: Session,
            skip: int = 0,
            limit: int = 100,
            organization_id: Optional[int] = None,
            status: Optional[str] = None,
            difficulty: Optional[str] = None
    ) -> List[Opportunity]:
        query = db.query(Opportunity)

        if organization_id:
            query = query.filter(Opportunity.organization_id == organization_id)

        if status:
            query = query.filter(Opportunity.status == status)

        if difficulty:
            query = query.filter(Opportunity.difficulty == difficulty)

        return query.offset(skip).limit(limit).all()

    @staticmethod
    def get_opportunities_with_organization(
            db: Session,
            skip: int = 0,
            limit: int = 100,
            status: Optional[str] = None,
    ) -> List:
        query = db.query(
            Opportunity,
            Organization.name.label('organization_name')
        ).join(Organization, Opportunity.organization_id == Organization.id)

        if status:
            query = query.filter(Opportunity.status == status)

        results = query.offset(skip).limit(limit).all()

        opportunities_with_org = []
        for opportunity, org_name in results:
            opportunity_dict = {**opportunity.__dict__}
            opportunity_dict['organization_name'] = org_name
            opportunities_with_org.append(opportunity_dict)

        return opportunities_with_org

    @staticmethod
    def create_opportunity(db: Session, opportunity: OpportunityCreate) -> Opportunity:
        final_points = opportunity.proposed_points

        db_opportunity = Opportunity(
            **opportunity.dict(),
            final_points = final_points,
            status = 'open'
        )

        db.add(db_opportunity)
        db.commit()
        db.refresh(db_opportunity)
        return db_opportunity

    @staticmethod
    def update_opportunity(
            db: Session,
            opportunity_id: int,
            opportunity_update: OpportunityUpdate
    ) -> Optional[Opportunity]:
        db_opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()

        if not db_opportunity:
            return None

        updated_data = opportunity_update.dict(exclude_unset=True)

        for field, value in updated_data.items():
            setattr(db_opportunity, field, value)

        db_opportunity.updated_at = datetime.now()
        db.commit()
        db.refresh(db_opportunity)
        return db_opportunity

    @staticmethod
    def delete_opportunity(db: Session, opportunity_id: int) -> bool:
        db_opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()

        if not db_opportunity:
            return False

        db.delete(db_opportunity)
        db.commit()
        return True

    @staticmethod
    def close_opportunity(db: Session, opportunity_id: int) -> Optional[Opportunity]:
        db_opportunity = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()

        if not db_opportunity:
            return None

        db_opportunity.status = 'closed'
        db_opportunity.updated_at = datetime.now()
        db.commit()
        db.refresh(db_opportunity)
        return db_opportunity

    @staticmethod
    def get_upcoming_opportunities(db: Session, limit: int = 10) -> List[Opportunity]:
        return db.query(Opportunity).filter(
            and_(
                Opportunity.status == 'open',
                Opportunity.date_start > datetime.now()
            )
        ).order_by(Opportunity.date_start.asc()).limit(limit).all()

    @staticmethod
    def count_opportunities_by_status(db: Session) -> dict:
        results = db.query(
            Opportunity.status,
            func.count(Opportunity.id)
        ).group_by(Opportunity.status).all()

        return {status: count for status, count in results}
