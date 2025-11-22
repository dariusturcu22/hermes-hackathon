from sqlalchemy import Column, Integer, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from ..applications.schema import ApplicationStatus
from ..database import Base


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    opportunity_id = Column(Integer, ForeignKey("events.id"), nullable=False)

    status = Column(
        Enum(ApplicationStatus),
        default=ApplicationStatus.PENDING,
        nullable=False
    )
    # "pending", "accepted", "rejected", "completed", "no_show"
    applied_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    # Relationships
    user = relationship("User", back_populates="applications")
    opportunity = relationship("Event", back_populates="applications")
