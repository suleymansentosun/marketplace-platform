from sqlalchemy.orm.session import Session
from schemas import AdvertisementBase, CategoryBase
from db.models import DbAdvertisement, DbCategory
from fastapi import HTTPException, status


def create_category(db: Session, request: CategoryBase):
  new_category = DbCategory(
    name = request.name,
  )
  db.add(new_category)
  db.commit()
  db.refresh(new_category)
  return new_category

def get_all_categories(db: Session):
  return db.query(DbCategory).all()

def get_category(db: Session, id: int):
  return db.query(DbCategory).filter(DbCategory.id == id).first()

def update_advertisement(db: Session, id: int, request: CategoryBase):
  category = db.query(DbCategory).filter(DbCategory.id == id)
  category.update(
    {
      DbCategory.name: request.name,
    }
  )
  db.commit()
  return 'Database is updated!'