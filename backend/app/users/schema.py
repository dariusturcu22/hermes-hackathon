from datetime import datetime
from typing import Optional, Literal, List
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    auth0_id: str
    name: str = None
    email: EmailStr = None
    role: Literal["volunteer", "organizer"] = None
    total_points: int = 0


class UserCreate(UserBase):
    """Schema for creating a new user"""
    pass


class UserUpdate(BaseModel):
    """Schema for updating user fields"""
    name: Optional[str] = Field(None, max_length=128)
    email: Optional[EmailStr] = Field(None, max_length=256)
    role: Optional[Literal["volunteer", "organizer"]] = None
    total_points: Optional[int] = Field(None, ge=0)


class UserInDB(UserBase):
    """Schema representing a user stored in DB"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class UserOut(BaseModel):
    """Schema for returning user data in API responses"""
    success: bool
    data: UserInDB


class UserListOut(BaseModel):
    success: bool
    data: List[UserInDB]
    total: int
