from cmath import log
from typing import List
from urllib import request
from fastapi import APIRouter, Depends, HTTPException, status
from db.db_user import get_user_ids
from db.models import DbReview
from schemas import ReviewBase, ReviewDisplay, ReviewUpdateDisplay
from db import db_reviews
from db.database import get_db
from sqlalchemy.orm import Session
import logging


router = APIRouter(
    prefix='/reviews',
    tags=['reviews']
)

# Post a review
@router.post('/', response_model=ReviewDisplay)
def create_post(request: ReviewBase, db: Session = Depends(get_db)):
    if request.reviewer_id == request.reviewed_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='You are not allowed to review yourself')
    return db_reviews.create_review(db, request)

# Get all reviews
@router.get('/', response_model=List[ReviewBase])
def get_all_reviews(db: Session = Depends(get_db)):
    return db_reviews.get_all_reviews(db)

# Get review
@router.get('/{id}', response_model=ReviewDisplay)
def get_review(id: int, db: Session = Depends(get_db)):
    return db_reviews.get_review(db, id)

# Update review
@router.put('/{id}/update')
def update_review(id: int, request: ReviewUpdateDisplay,  db: Session = Depends(get_db)):
   # logger.info(request.rating)
    if request.rating < 1  or  request.rating > 5:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Raitng should be between 1 and 5')
        
    return db_reviews.update_review(db, id, request)

# Delete review
@router.delete('/delete/{id}')
def delete_review(id: int, db: Session = Depends(get_db)):
    return db_reviews.delete_review(db, id)

