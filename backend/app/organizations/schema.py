from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class OrganizationBase(BaseModel):
    name: str
    description: str
    owner_user_id: int
    verified: bool = False


class OrganizationCreate(OrganizationBase):
    pass


class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    owner_user_id: Optional[int] = None
    verified: Optional[bool] = None


class OrganizationInDB(OrganizationBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class OrganizationOut(BaseModel):
    success: bool
    data: OrganizationInDB


class OrganizationListOut(BaseModel):
    success: bool
    data: List[OrganizationInDB]
    total: int
