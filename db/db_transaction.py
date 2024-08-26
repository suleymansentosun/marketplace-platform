from sqlalchemy import desc
from sqlalchemy.orm.session import Session
from schemas import TransactionBase
from db.models import DbTransaction

# Ödeme talebini bir mesaj tipi yapabiliriz.

def create_transaction(db: Session, payment_amount, conversation_id):
  new_transaction = DbTransaction(
    payment_amount = payment_amount,
    conversation_id = conversation_id,
    status = "proposal_sended"
  )
  db.add(new_transaction)
  db.commit()
  db.refresh(new_transaction)
  return new_transaction

def get_all_transactions(db: Session):
  return db.query(DbTransaction).all()

def get_transaction(db: Session, id: int):
  return db.query(DbTransaction).filter(DbTransaction.id == id).first()

def get_transactions_for_conversation(db: Session, conversation_id: int):
    return db.query(DbTransaction).filter(DbTransaction.conversation_id == conversation_id).all()

def get_last_transaction_in_specific_conversation(db: Session, conversation_id: int):
  return db.query(DbTransaction).filter(DbTransaction.conversation_id == conversation_id).order_by(
            desc(DbTransaction.created_at)).first()

