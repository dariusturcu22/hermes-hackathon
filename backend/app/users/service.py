from fastapi import HTTPException

from backend.app.users.schema import UserCreate, UserBase, UserUpdate, UserDelete, UserInDB
from sqlalchemy.orm import Session
from model import User

def create_user(db:Session, user: UserCreate):
    db_user = db.query(User).filter(User.auth0_id == user.auth0_id).first()
    if db_user:
        raise HTTPException(status_code=400, detail="auth0_id already registered")

    # new_user = UserInDB()
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_user(db:Session):
    return db.query()