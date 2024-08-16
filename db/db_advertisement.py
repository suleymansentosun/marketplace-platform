from sqlalchemy.orm.session import Session
from schemas import AdvertisementBase
from db.models import DbAdvertisement
from fastapi import HTTPException, status
from typing import Optional


def create_advertisement(db: Session, request: AdvertisementBase):
  new_advertisement = DbAdvertisement(
    title = request.title,
    price = request.price,
    description = request.description,
    condition = request.condition,
    delivery = request.delivery,
    category_id = request.category_id
  )
  db.add(new_advertisement)
  db.commit()
  db.refresh(new_advertisement)
  return new_advertisement

def get_all_advertisements(db: Session):
  return db.query(DbAdvertisement).all()

def get_advertisement(db: Session, id: int):
  return db.query(DbAdvertisement).filter(DbAdvertisement.id == id).first()

def update_advertisement(db: Session, id: int, request: AdvertisementBase):
  advertisement = db.query(DbAdvertisement).filter(DbAdvertisement.id == id)
  advertisement.update(
    {
      DbAdvertisement.title: request.title,
      DbAdvertisement.price: request.price,
      DbAdvertisement.description: request.description,
      DbAdvertisement.condition: request.condition,
      DbAdvertisement.delivery: request.delivery,
      DbAdvertisement.category_id: request.category_id,
    }
  )
  db.commit()
  return 'Database is updated!'

def delete_advertisement(db: Session, id: int):
   advertisement = db.query(DbAdvertisement).filter(DbAdvertisement.id == id).first()
   db.delete(advertisement)
   db.commit()
   return 'the advertisement has been deleted!'

def search_advertisements_by_name(db: Session, search_query: str):
    return db.query(DbAdvertisement).filter(DbAdvertisement.title.like(f"{search_query}%")).all()

def filter_advertisements(db: Session, category_id: Optional[int] = None, min_price: Optional[int] = None, max_price: Optional[int] = None):
    query = db.query(DbAdvertisement)
    if category_id is not None:
        query = query.filter(DbAdvertisement.category_id == category_id)
    if min_price is not None:
        query = query.filter(DbAdvertisement.price >= min_price)
    if max_price is not None:
        query = query.filter(DbAdvertisement.price <= max_price)
    return query.all()