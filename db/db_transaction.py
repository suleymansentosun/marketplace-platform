from sqlalchemy.orm.session import Session
from schemas import TransactionBase
from db.models import DbTransaction

def create_transaction(db: Session, request: TransactionBase):
  new_transaction = DbTransaction(
    payment_amount = request.payment_amount,
    advertisement_id = request.advertisement_id
  )
  db.add(new_transaction)
  db.commit()
  db.refresh(new_transaction)
  return new_transaction

def get_all_transactions(db: Session):
  return db.query(DbTransaction).all()

def get_transaction(db: Session, id: int):
  return db.query(DbTransaction).filter(DbTransaction.id == id).first()

