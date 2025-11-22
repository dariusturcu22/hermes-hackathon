from fastapi import HTTPException

from backend.app.users.schema import UserCreate, UserBase, UserUpdate, UserDelete
from sqlalchemy.orm import Session
from model import User

def create_user(user: UserCreate, db: Session):
    db_user = db.query(User).filter(User.auth0_id == user.auth0_id).first()
    if db_user:
        raise HTTPException(status_code=400, detail="auth0_id already registered")

    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_users(db:Session):
    return db.query(User).all()

def get_user(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def update_user(user_id: int, user_update: UserUpdate, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user_update.items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user

def delete_user(user_id: int, db: Session):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return user