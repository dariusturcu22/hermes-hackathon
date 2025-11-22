from fastapi import Depends
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.main import app
from schema import UserCreate, UserUpdate, UserBase, UserDelete, UserOut
import service

# Create a new user
@app.post("/users/", response_model=UserBase)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    return service.create_user(user, db)

# Get all users
@app.get("/users/", response_model=list[UserOut])
def read_users(db: Session = Depends(get_db)):
    return service.get_users(db)

# Get a single user by ID
@app.get("/users/{user_id}", response_model=UserOut)
def read_user(user_id: int, db: Session = Depends(get_db)):
    return service.get_user(user_id, db)

# Update a user
@app.put("/users/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_update: UserUpdate, db: Session = Depends(get_db)):
    return service.update_user(user_id, user_update, db)

# Delete a user
@app.delete("/users/{user_id}", response_model=UserOut)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    return service.delete_user(user_id, db)
