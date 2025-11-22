from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..organizations.service import OrganizationService
from ..organizations.schema import (
    OrganizationCreate,
    OrganizationUpdate,
    OrganizationOut,
    OrganizationListOut,
    OrganizationDelete
)

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.post("/", response_model=OrganizationOut, status_code=201)
def create_organization(data: OrganizationCreate, db: Session = Depends(get_db)):
    item = OrganizationService.create_organization(db, data)
    return {"success": True, "data": item}


@router.get("/", response_model=OrganizationListOut)
def get_organizations(db: Session = Depends(get_db)):
    items = OrganizationService.get_organizations(db)
    return {"success": True, "data": items}


@router.get("/{organization_id}", response_model=OrganizationOut)
def get_organization(organization_id: int, db: Session = Depends(get_db)):
    item = OrganizationService.get_organization(db, organization_id)
    if not item:
        raise HTTPException(status_code=404, detail="Organization not found")

    return {"success": True, "data": item}


@router.patch("/{organization_id}", response_model=OrganizationOut)
def update_organization(organization_id: int, data: OrganizationUpdate, db: Session = Depends(get_db)):
    item = OrganizationService.update_organization(db, organization_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="Organization not found")

    return {"success": True, "data": item}


@router.delete("/{organization_id}", response_model=OrganizationDelete)
def delete_organization(organization_id: int, db: Session = Depends(get_db)):
    success = OrganizationService.delete_organization(db, organization_id)
    if not success:
        raise HTTPException(status_code=404, detail="Organization not found")

    return {"success": True, "message": "Organization deleted successfully"}
