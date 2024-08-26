from fastapi import APIRouter, Depends, HTTPException, status
from auth.oauth2 import get_current_user
from db.database import get_db
from db.db_conversation import get_conversation_by_id
from db.db_message import get_messages_for_conversation
from db.db_transaction import get_transactions_for_conversation
from schemas import ConversationSpecificDisplay, MessageDisplay, TransactionDisplay, UserBase
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/conversation",
    tags=["conversation"]
)

@router.get("/{conversation_id}", response_model=ConversationSpecificDisplay)
def get_conversation(conversation_id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    conversation = get_conversation_by_id(db, conversation_id)

    if not conversation:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Conversation not found")

    if current_user.id != conversation.buyer_id and current_user.id != conversation.advertisement.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You do not have access to this conversation")

    messages = get_messages_for_conversation(db, conversation_id)
    message_displays = [MessageDisplay.model_validate(message) for message in messages]

    transactions = get_transactions_for_conversation(db, conversation_id)
    transaction_displays = [TransactionDisplay.model_validate(transaction) for transaction in transactions]

    # Return the conversation details, along with messages and transactions
    return ConversationSpecificDisplay(
        id = conversation.id,
        advertisement_id = conversation.advertisement_id,
        buyer_id = conversation.buyer_id,
        seller_id = conversation.advertisement.owner_id,
        messages = message_displays,
        transactions = transaction_displays
    )


