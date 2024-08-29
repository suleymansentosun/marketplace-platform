from db.hash import Hash
from sqlalchemy.orm.session import Session
from schemas import UserBase, UserDisplay
from db.models import DbUser, DbReview
from sqlalchemy import select
from sqlalchemy import func



def create_user(db: Session, request: UserBase):
    new_user = DbUser(
        username = request.username,
        email = request.email,
        password = Hash.bcrypt(request.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return UserDisplay(
        id=new_user.id,
        username=new_user.username,
        email=new_user.email,
        avarage_rating=0.0  
    )

def get_all_users(db: Session):
    return db.query(DbUser).all()

def get_user(db: Session, id: int):
    return db.query(DbUser).filter(DbUser.id == id).first()

def update_user(db: Session, id: int, request: UserBase):
    user = db.query(DbUser).filter(DbUser.id == id)
    user.update({
        
            DbUser.username: request.username,
            DbUser.email: request.email,
            DbUser.password: Hash.bcrypt(request.password)
        })
    db.commit()
    return "OK - Database is updated"

def delete_user(db: Session, id: int):
    user = db.query(DbUser).filter(DbUser.id == id).first()
    db.delete(user)
    db.commit()
    return'User deleted'

def get_user_ids(db: Session):
    user_ids = db.query(DbUser.id).all()
    return [user_id[0] for user_id in user_ids] 
    
    

