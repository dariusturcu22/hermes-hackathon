from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PointsHistoryBase(BaseModel):
    user_id: int
    event_id: int
    points_awarded: int
    reason: Optional[str] = None


class PointsHistoryCreate(PointsHistoryBase):
    pass


class PointsHistoryRead(PointsHistoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PointsHistoryUpdate(BaseModel):
    user_id: Optional[int] = None
    event_id: Optional[int] = None
    points_awarded: Optional[int] = None
    reason: Optional[str] = None
