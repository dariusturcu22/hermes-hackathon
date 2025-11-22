from pydantic import BaseModel, validator, field_validator
from datetime import datetime
from typing import Optional, List
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
    location: Optional[str] = None
    date_start: datetime
    date_end: datetime
    difficulty: DifficultyLevel
    duration_minutes: int
    proposed_points: int
    max_participants: Optional[int] = None

    @field_validator('date_end')
    def validate_dates(cls, v, values):
        if 'date_start' in values and v <= values['date_start']:
            raise ValueError('date_end must be after date_start')
        return v

    @field_validator('proposed_points')
    def validate_points(cls, v):
        if v < 0:
            raise ValueError('Points cannot be negative')
        return v

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
    organization_name: str

class EventOut(BaseModel):
    success: bool
    data: EventInDB

class EventListOut(BaseModel):
    success: bool
    data: List[EventWithOrganization]
    total: int