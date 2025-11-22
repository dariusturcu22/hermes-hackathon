from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from ..database import Base


class PointsHistory(Base):
    __tablename__ = "points_history"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("opportunities.id"), nullable=True)
    points_awarded = Column(Integer, nullable=False)
    reason = Column(String(128), nullable=True)
    created_at = Column(DateTime, server_default=func.now())

    user = relationship("User", back_populates="points_history")
    opportunity = relationship("Opportunity", back_populates="points_history")