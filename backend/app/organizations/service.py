from sqlalchemy.orm import Session
from .model import Organization
from .schema import OrganizationCreate, OrganizationUpdate


def create_organization(db: Session, organization: OrganizationCreate):
    organization = Organization(**organization.model_dump())
    db.add(organization)
    db.commit()
    db.refresh(organization)
    return organization


def get_organizations(db: Session):
    return db.query(Organization).all()


def get_organization(db: Session, organization_id: int):
    return db.query(Organization).filter(Organization.id == organization_id).first()


def update_organization(db: Session, organization_id: int, data: OrganizationUpdate):
    organization = get_organization(db, organization_id)
    if not organization:
        return None

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(organization, key, value)

    db.commit()
    db.refresh(organization)
    return organization


def delete_organization(db: Session, organization_id: int):
    organization = get_organization(db, organization_id)
    if not organization:
        return False

    db.delete(organization)
    db.commit()
    return True