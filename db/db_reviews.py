from db.hash import Hash
from sqlalchemy.orm.session import Session
from schemas import ReviewBase, ReviewDisplay
from db.models import DbReview
from fastapi import Depends
from db.database import get_db

# Post review
def create_review(db: Session, request: ReviewBase ):
    review = DbReview(
        rating=request.rating, 
        review_content= request.review_content,
        reviewer_id = request.reviewer_id,
        reviewed_user_id = request.reviewed_user_id
    )
    db.add(review)
    db.commit()
    db.refresh(review)
    return review
