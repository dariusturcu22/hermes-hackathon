from sqlalchemy import Column, Integer, String, DateTime, func
from ..database import Base

class User(Base):
    # __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    auth0_id = Column(String(128), unique=True, nullable=False)
    name = Column(String(128), nullable=False)
    email = Column(String(256), unique=True, nullable=True)
    role = Column(String(32), nullable=False)  # "volunteer" or "organizer"
    total_points = Column(Integer, default=0)

    created_at = Column(DateTime, default=func.now(), nullable=False)
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)