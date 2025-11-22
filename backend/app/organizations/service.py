from sqlalchemy.orm import Session
from ..organizations.model import Organization
from ..organizations.schema import OrganizationCreate, OrganizationUpdate


class OrganizationService:
    @staticmethod
    def create_organization(db: Session, data: OrganizationCreate):
        organization = Organization(**data.model_dump())
        db.add(organization)
        db.commit()
        db.refresh(organization)
        return organization

    @staticmethod
    def get_organizations(db: Session):
        return db.query(Organization).all()

    @staticmethod
    def get_organization(db: Session, organization_id: int):
        return db.query(Organization).filter(Organization.id == organization_id).first()

    @staticmethod
    def update_organization(db: Session, organization_id: int, data: OrganizationUpdate):
        organization = OrganizationService.get_organization(db, organization_id)
        if not organization:
            return None

        update_data = data.model_dump(exclude_unset=True)
        for k, v in update_data.items():
            setattr(organization, k, v)

        db.commit()
        db.refresh(organization)
        return organization

    @staticmethod
    def delete_organization(db: Session, organization_id: int):
        organization = OrganizationService.get_organization(db, organization_id)
        if not organization:
            return False

        db.delete(organization)
        db.commit()
        return True
