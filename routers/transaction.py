from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from db import db_advertisement, db_transaction
from fastapi import HTTPException
from typing import List
from schemas import TransactionBase, TransactionDisplay

router = APIRouter(
    prefix="/transaction",
    tags=["transaction"]
)

@router.post('/', response_model= TransactionDisplay)
def create_transaction(request: TransactionBase, db: Session = Depends(get_db)):
    advertisement = db_advertisement.get_advertisement(db, request.advertisement_id)
    if advertisement is None:
        raise HTTPException(status_code=404, detail="Product is not found")
    return db_transaction.create_transaction(db, request)

@router.get('/', response_model=List[TransactionDisplay])
def get_all_transactions(db: Session = Depends(get_db)):
    return db_transaction.get_all_transactions(db)

@router.get('/{id}', response_model=TransactionDisplay)
def get_transaction(id: int, db: Session = Depends(get_db)):
    return db_transaction.get_transaction(db, id)