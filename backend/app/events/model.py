from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from ..database import Base

class Event(Base):
    __tablename__ = 'events'
    id = Column(Integer, primary_key=True, autoincrement=True)
    organization_id = Column(Integer, ForeignKey('organizations.id'), nullable=False)

    title = Column(String(128), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(256), nullable=True)
    date_start = Column(DateTime, nullable=False)
    date_end = Column(DateTime, nullable=False)

    difficulty = Column(String(32))  # "easy", "medium", "hard"
    duration_minutes = Column(Integer, nullable=False)
    proposed_points = Column(Integer, nullable=False)
    final_points = Column(Integer, nullable=False)

    max_participants = Column(Integer, nullable=True)
    status = Column(String(32), default="open")

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    organization = relationship("Organization", back_populates="events")
    applications = relationship("Application", back_populates="event", cascade="all, delete-orphan")
    points_history = relationship("PointsHistory", back_populates="event", cascade="all, delete-orphan")
