from sqlalchemy import desc
from sqlalchemy.orm.session import Session
from db.models import DbMessage
from schemas import MessageBase

def get_messages_for_conversation(db: Session, conversation_id: int):
    return db.query(DbMessage).filter(DbMessage.conversation_id == conversation_id).all()

def get_last_message_for_conversation(db: Session, conversation_id: int):
    return db.query(DbMessage).filter(DbMessage.conversation_id == conversation_id).order_by(
            desc(DbMessage.created_at)).first()

def create_message(db: Session, request: MessageBase, conversation_id):
    new_message = DbMessage(
        conversation_id = conversation_id,
        content = request.content,
        sender_user_id = request.sender_user_id,
    )
    db.add(new_message)
    db.commit()
    db.refresh(new_message)
    return new_message