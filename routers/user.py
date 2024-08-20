from this import d
from typing import List
from fastapi import APIRouter, Depends
from schemas import UserBase, UserDisplay
from db import db_user
from db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/user',
    tags=['user']
)

# Create uer
@router.post('/', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)

# Get all users
@router.get('/', response_model=List[UserDisplay])
def get_all_users(db: Session = Depends(get_db)):
    return db_user.get_all_users(db)

# Get user
@router.get('/{id}', response_model=UserDisplay)
def get_user(id: int, db: Session = Depends(get_db)):
    return db_user.get_user(db, id)

# Update user
@router.put('/{id}/update')
def update_user(id: int, request: UserBase,  db: Session = Depends(get_db)):
    return db_user.update_user(db, id, request)