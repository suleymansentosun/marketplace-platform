from typing import List
from fastapi import APIRouter, Depends
from schemas import UserAllDisplay, UserBase, UserDisplay
from db import db_user
from db.database import get_db
from sqlalchemy.orm import Session
from db.db_user import get_user
from db.db_reviews import get_filtered_reviews
import sys

sys.setrecursionlimit(10000)

router = APIRouter(
    prefix='/user',
    tags=['user']
)

# Create uer
@router.post('/', response_model=UserDisplay)
def create_user(request: UserBase, db: Session = Depends(get_db)):
    return db_user.create_user(db, request)

# Get all users
@router.get('/', response_model=List[UserAllDisplay])
def get_all_users(db: Session = Depends(get_db)):
    users: List[UserAllDisplay] = db_user.get_all_users(db)
    for user in users:
        average_rating = get_filtered_reviews(db, user.id)
        user.avarage_rating = average_rating
    return users
    
# Get user
@router.get('/{id}', response_model=UserDisplay)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db_user.get_user(db, id)
    average_rating = get_filtered_reviews(db, id)
    return UserDisplay(
        id=user.id,
        username=user.username,
        email=user.email,  
        avarage_rating=average_rating 
    )
    
# Update user
@router.put('/{id}/update')
def update_user(id: int, request: UserBase,  db: Session = Depends(get_db)):
    return db_user.update_user(db, id, request)

# Delete user
@router.delete('/delete/{id}')
def delete_user(id: int, db: Session = Depends(get_db)):
    return db_user.delete_user(db, id)
 