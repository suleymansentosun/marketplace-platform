from typing import List
from schemas import AdvertisementBase, AdvertisementListDisplay, AdvertisementDetailDisplay, UserBase
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_advertisement, db_category
from typing import Optional
from auth.oauth2 import get_current_user, oauth2_scheme

router = APIRouter(
    prefix="/advertisement",
    tags=["advertisement"]
)

@router.post('/', response_model= AdvertisementDetailDisplay)
def create_advertisement(request: AdvertisementBase, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme), current_user: UserBase = Depends(get_current_user)):
    category = db_category.get_category(db, request.category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    
    if request.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to do this operation")

    return db_advertisement.create_advertisement(db, request)

@router.get('/', response_model=List[AdvertisementListDisplay])
def get_all_advertisements(db: Session = Depends(get_db)):
    return db_advertisement.get_all_advertisements(db)

@router.get('/{id}', response_model=AdvertisementDetailDisplay)
def get_advertisement(id: int, db: Session = Depends(get_db)):
    return db_advertisement.get_advertisement(db, id)

@router.put('/{id}')
def update_advertisement(id: int, request: AdvertisementBase, db: Session = Depends(get_db)):
    return db_advertisement.update_advertisement(db, id, request)

@router.delete('/{id}')
def delete(id: int, db: Session = Depends(get_db)):
    return db_advertisement.delete_advertisement(db, id)

@router.get("/search/", response_model=List[AdvertisementListDisplay])
def search_advertisements(search_query: str, db: Session = Depends(get_db)):
    advertisements = db_advertisement.search_advertisements_by_name(db, search_query)
    if not advertisements:
        raise HTTPException(status_code=404, detail="No advertisements found")
    return advertisements

@router.get("/filter/", response_model=List[AdvertisementListDisplay])
def filter_advertisements(category_id: Optional[int] = None, min_price: Optional[int] = None, 
                          max_price: Optional[int] = None, db: Session = Depends(get_db)):
    advertisements = db_advertisement.filter_advertisements(db, category_id, min_price, max_price)
    if not advertisements:
        raise HTTPException(status_code=404, detail="No advertisements found for the given category")
    return advertisements