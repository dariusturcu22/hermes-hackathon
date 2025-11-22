from pydantic import BaseModel, field_validator, model_validator
from typing import Optional, List
from datetime import datetime
from enum import Enum


class DifficultyLevel(str, Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


class EventStatus(str, Enum):
    OPEN = "open"
    CLOSED = "closed"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class EventBase(BaseModel):
    title: str
    description: str
    location: str
    date_start: datetime
    date_end: datetime
    difficulty: str
    duration_minutes: int
    proposed_points: int
    max_participants: int
    organization_id: int

    @model_validator(mode="after")
    def check_dates(self):
        if self.date_end <= self.date_start:
            raise ValueError("date_end must be after date_start")
        return self


class EventCreate(EventBase):
    organization_id: int


class EventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    date_start: Optional[datetime] = None
    date_end: Optional[datetime] = None
    difficulty: Optional[DifficultyLevel] = None
    duration_minutes: Optional[int] = None
    proposed_points: Optional[int] = None
    final_points: Optional[int] = None
    max_participants: Optional[int] = None
    status: Optional[EventStatus] = None


class EventInDB(EventBase):
    id: int
    organization_id: int
    final_points: int
    status: EventStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EventWithOrganization(EventInDB):
    organization_name: Optional[str] = None

    class Config:
        from_attributes = True


class EventOut(BaseModel):
    success: bool
    data: EventInDB


class EventListOut(BaseModel):
    success: bool
    data: List[EventWithOrganization]
    total: int
