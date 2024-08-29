from db.hash import Hash
from sqlalchemy.orm.session import Session
from schemas import ReviewBase, ReviewDisplay
from db.models import DbReview
from sqlalchemy import func


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

# Get all reviews
def get_all_reviews(db: Session):
    return db.query(DbReview).all()

# Get all reviews
def get_review(db: Session, id: int):
    return db.query(DbReview).filter(DbReview.id == id).first()

# Update review
def update_review(db: Session, id: int, request: ReviewBase):
    review = db.query(DbReview).filter(DbReview.id == id)
    review.update({
        
            DbReview.rating: request.rating,
            DbReview.review_content: request.review_content,
           
        })
    db.commit()
    return "Your review is updated"

# Delete review
def delete_review(db: Session, id: int):
    review = db.query(DbReview).filter(DbReview.id == id).first()
    db.delete(review)
    db.commit()
    return'Your review is deleted'

def get_filtered_reviews(db: Session, user_id: int):
    average_rating = db.query(func.avg(DbReview.rating)).filter(DbReview.reviewed_user_id == user_id).scalar()
    return average_rating

