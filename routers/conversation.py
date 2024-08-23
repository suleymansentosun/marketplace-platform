from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db import models
from db.database import get_db
from sqlalchemy.orm import joinedload
from schemas import ConversationDisplay

router = APIRouter(
    prefix="/conversation",
    tags=["conversation"]
)

@router.get("/conversations", response_model=List[ConversationDisplay])
def get_conversations(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    conversations = db.query(models.DbConversation).options(
        joinedload(models.DbConversation.advertisement)
    ).filter(
        (models.DbConversation.buyer_id == current_user.id) | 
        (models.DbAdvertisement.seller_id == current_user.id)
    ).all()
    
    # Convert to a list of ConversationResponse objects, including the seller_id from the Product
    conversation_responses = []
    for conversation in conversations:
        conversation_responses.append(
            ConversationDisplay(
                id=conversation.id,
                advertisement_id=conversation.advertisement_id,
                buyer_id=conversation.buyer_id,
                seller_id=conversation.advertisement.seller_id  # Access seller_id from the related product
            )
        )

    return conversation_responses
