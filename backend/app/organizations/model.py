from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, DateTime, func
from ..database import Base


class Organization(Base):
    __tablename__ = 'organizations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(128), nullable=False)
    description = Column(String, nullable=False)
    owner_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    verified = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())