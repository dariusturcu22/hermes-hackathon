from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.users.service import UserService
from backend.app.users.schema import (
    UserCreate,
    UserUpdate,
    UserOut,
    UserListOut
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserOut, status_code=201)
def create_user(data: UserCreate, db: Session = Depends(get_db)):
    item = UserService.create_user(db, data)
    return {"success": True, "data": item}


@router.get("/", response_model=UserListOut)
def list_users(db: Session = Depends(get_db)):
    items = UserService.get_users(db)
    return {"success": True, "data": items, "total": len(items)}


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    item = UserService.get_user(db, user_id)
    if not item:
        raise HTTPException(status_code=404, detail="User not found")

    return {"success": True, "data": item}


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, data: UserUpdate, db: Session = Depends(get_db)):
    item = UserService.update_user(db, user_id, data)
    if not item:
        raise HTTPException(status_code=404, detail="User not found")

    return {"success": True, "data": item}


@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    success = UserService.delete_user(db, user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")

    return {"success": True, "message": "User deleted successfully"}
