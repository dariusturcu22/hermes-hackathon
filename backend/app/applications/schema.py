from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum

class ApplicationStatus(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    COMPLETED = "completed"
    NO_SHOW = "no_show"

class ApplicationBase(BaseModel):
    status: ApplicationStatus = ApplicationStatus.PENDING

class ApplicationCreate(BaseModel):
    user_id: int
    event_id: int

class ApplicationUpdate(BaseModel):
    status: Optional[ApplicationStatus] = None

class ApplicationInDB(ApplicationBase):
    id: int
    user_id: int
    event_id: int
    applied_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ApplicationWithDetails(ApplicationInDB):
    user_name: str
    user_email: str
    event_title: str
    organization_name: str
    event_final_points: int

class ApplicationResponse(BaseModel):
    success: bool
    data: ApplicationInDB

class ApplicationWithDetailsResponse(BaseModel):
    success: bool
    data: ApplicationWithDetails

class ApplicationListResponse(BaseModel):
    success: bool
    data: List[ApplicationWithDetails]
    total: int

class ApplicationStatsResponse(BaseModel):
    success: bool
    data: dict