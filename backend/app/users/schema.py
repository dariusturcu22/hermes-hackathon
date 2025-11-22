from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    auth0_id: str = Field(..., max_length=128)
    name: str = Field(None, max_length=128)
    email: Optional[EmailStr] = Field(None, max_length=256)
    role: Literal["volunteer", "organizer"] = None
    total_points: int = Field(default=0, ge=0)

class UserCreate(UserBase):
    """Schema for creating a new user"""
    pass

class UserUpdate(BaseModel):
    """Schema for updating user fields"""
    name: Optional[str] = Field(None, max_length=128)
    email: Optional[EmailStr] = Field(None, max_length=256)
    role: Optional[Literal["volunteer", "organizer"]] = None
    total_points: Optional[int] = Field(None, ge=0)

class UserDelete(BaseModel):
    id: int
    pass

class UserInDB(UserBase):
    """Schema representing a user stored in DB"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserOut(UserBase):
    """Schema for returning user data in API responses"""
    pass
