from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class OrganizationBase(BaseModel):
    name: str
    description: str
    owner_user_id: int
    verified: bool = False

class OrganizationCreate(OrganizationBase):
    pass

class OrganizationRead(BaseModel):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class OrganizationUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    owner_user_id: Optional[int] = None
    verified: Optional[bool] = None