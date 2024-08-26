from sqlalchemy.orm.session import Session
from sqlalchemy.orm import joinedload
from db.models import DbConversation, DbAdvertisement, DbMessage, DbTransaction

def get_conversation_by_id(db: Session, conversation_id: int):
    return db.query(DbConversation).options(
        joinedload(DbConversation.advertisement)
    ).filter(DbConversation.id == conversation_id).first()

def get_conversation_by_product_id(db: Session, advertisement_id: int):
    return db.query(DbConversation).filter(
        DbConversation.advertisement_id == advertisement_id,
    ).first()

def get_conversations_for_user(db: Session, user_id: int):
    return db.query(DbConversation).options(
        joinedload(DbConversation.advertisement)
    ).filter(
        (DbConversation.buyer_id == user_id) | 
        (DbAdvertisement.owner_id == user_id)
    ).all()

def create_conversation(db: Session, advertisement_id: int, buyer_id: int):
    new_conversation = DbConversation(advertisement_id=advertisement_id, buyer_id=buyer_id)
    db.add(new_conversation)
    db.commit()
    db.refresh(new_conversation)
    return new_conversation




