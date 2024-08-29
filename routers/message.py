from fastapi import APIRouter
from auth.oauth2 import get_current_user
from db import db_message
from db.database import get_db
from db.db_advertisement import get_advertisement
from db.db_conversation import create_conversation, get_conversation_by_id, get_conversation_by_product_id, get_specific_conversation
from db.db_message import create_message
from db.models import DbConversation, DbMessage
from schemas import MessageBase, MessageDisplay, UserBase
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(
    prefix="/message",
    tags=["message"]
)

@router.post("/", response_model=MessageDisplay)
def send_message(request: MessageBase, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    if current_user.id != request.sender_user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this conversation")

    advertisement = get_advertisement(db, request.advertisement_id)
    if not advertisement:
        raise HTTPException(status_code=404, detail="Advertisement not found.")
            
    conversation = get_specific_conversation(db, advertisement.id, request.buyer_user_id)
    if not conversation:
        if request.buyer_user_id != request.sender_user_id and request.buyer_user_id != advertisement.owner_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You cannot start a conversation as a seller!")
        conversation = create_conversation(db, advertisement.id, request.buyer_user_id)
    else:
        if request.sender_user_id != advertisement.owner_id and request.sender_user_id != conversation.buyer_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this conversation!")

    return db_message.create_message(db, request, conversation.id)