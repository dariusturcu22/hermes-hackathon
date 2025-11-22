from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from . import service
from .schema import OrganizationCreate, OrganizationRead, OrganizationUpdate


router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post("/", response_model=OrganizationRead, status_code=status.HTTP_201_CREATED)
def create_organization(data: OrganizationCreate, db: Session = Depends(get_db)):
    return service.create_organization(db, data)


@router.get("/", response_model=list[OrganizationRead])
def list_organizations(db: Session = Depends(get_db)):
    return service.get_organizations(db)


@router.get("/{organization_id}", response_model=OrganizationRead)
def get_organization(organization_id: int, db: Session = Depends(get_db)):
    organization = service.get_organization(db, organization_id)
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

    return organization


@router.patch("/{organization_id}", response_model=OrganizationRead)
def update_organization(organization_id: int, data: OrganizationUpdate, db: Session = Depends(get_db)):
    organization = service.update_organization(db, organization_id, data)
    if not organization:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

    return organization


@router.delete("/{organization_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_organization(organization_id: int, db: Session = Depends(get_db)):
    success = service.delete_organization(db, organization_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Organization not found")

    return None
