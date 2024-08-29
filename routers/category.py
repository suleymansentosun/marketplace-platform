from typing import List
from schemas import AdvertisementBase, AdvertisementListDisplay, AdvertisementDetailDisplay, CategoryBase, CategoryDisplay
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_advertisement, db_category

router = APIRouter(
    prefix="/category",
    tags=["category"]
)

@router.post('/', response_model= CategoryDisplay)
def create_category(request: CategoryBase, db: Session = Depends(get_db)):
    return db_category.create_category(db, request)

@router.get('/', response_model=List[CategoryDisplay])
def get_all_categories(db: Session = Depends(get_db)):
    return db_category.get_all_categories(db)

@router.put('/{id}')
def update_category(id: int, request: CategoryBase, db: Session = Depends(get_db)):
    return db_category.update_advertisement(db, id, request)