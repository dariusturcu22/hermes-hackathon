from fastapi import HTTPException
from sqlalchemy.orm import Session

from backend.app.users.model import User
from backend.app.users.schema import UserCreate, UserUpdate


class UserService:
    @staticmethod
    def create_user(db: Session, data: UserCreate):
        existing = db.query(User).filter(User.auth0_id == data.auth0_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="auth0_id already registered")

        user = User(**data.model_dump())
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_users(db: Session):
        return db.query(User).all()

    @staticmethod
    def get_user(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user

    @staticmethod
    def update_user(db: Session, user_id: int, data: UserUpdate):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(user, key, value)

        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def delete_user(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        db.delete(user)
        db.commit()
        return True
