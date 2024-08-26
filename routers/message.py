from fastapi import APIRouter
from auth.oauth2 import get_current_user
from db.database import get_db
from db.db_advertisement import get_advertisement
from db.db_conversation import create_conversation, get_conversation_by_id, get_conversation_by_product_id
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
def send_message(request: MessageBase, advertisement_id: int, 
                 db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):

    advertisement = get_advertisement(db, advertisement_id)
    if not advertisement:
        raise HTTPException(status_code=404, detail="Advertisement not found.")
    
    if advertisement.owner_id == current_user.id:
        buyer_id = request.sender_user_id
    else:
        buyer_id = current_user.id
    
    conversation = get_conversation_by_product_id(db, advertisement_id=advertisement.id)
    if not conversation:
        conversation = create_conversation(db, advertisement_id=advertisement.id, buyer_id=buyer_id)

    new_message = create_message(db, conversation.id, request.content, request.sender_user_id)
    return new_message