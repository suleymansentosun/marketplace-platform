from this import d
from typing import List
from fastapi import APIRouter, Depends
from schemas import ReviewBase, ReviewDisplay
from db import db_reviews
from db.database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix='/reviews',
    tags=['reviews']
)

# Post a review
@router.post('/', response_model=ReviewDisplay)
def create_post(request: ReviewBase, db: Session = Depends(get_db)):
    #request.reviewer_id = current_user.id
    return db_reviews.create_review(db, request)