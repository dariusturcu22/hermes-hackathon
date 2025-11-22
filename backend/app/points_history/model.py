from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base


class PointsHistory(Base):
    __tablename__ = "points_history"
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    points_awarded = Column(Integer, nullable=False)
    reason = Column(String(128), nullable=True)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="points_history")
    event = relationship("Event", back_populates="points_history")
