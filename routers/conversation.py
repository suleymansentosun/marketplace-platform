from fastapi import APIRouter, Depends, HTTPException, status
from auth.oauth2 import get_current_user
from db.database import get_db
from db.db_conversation import get_conversation_by_id
from db.db_message import get_messages_for_conversation
from db.db_payment_request import create_payment_proposal, get_conversation_payment_proposals
from db.models import DbConversation
from schemas import ConversationSpecificDisplay, MessageDisplay, PaymentProposalCreate, PaymentProposalDisplay, UserBase
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

    payment_proposals = get_conversation_payment_proposals(db, conversation_id)
    payment_proposals_displays = [PaymentProposalDisplay.model_validate(payment_proposal) for payment_proposal in payment_proposals]

    # Return the conversation details, along with messages and transactions
    return ConversationSpecificDisplay(
        id = conversation.id,
        advertisement_id = conversation.advertisement_id,
        buyer_id = conversation.buyer_id,
        seller_id = conversation.advertisement.owner_id,
        messages = message_displays,
        payment_proposals = payment_proposals_displays
    )

@router.post("/{conversation_id}/payment-proposal", response_model=PaymentProposalDisplay)
def send_payment_proposal(conversation_id: int, request: PaymentProposalCreate, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    conversation = db.query(DbConversation).filter(DbConversation.id == conversation_id).first()
    
    if not conversation or (conversation.buyer_id != current_user.id and conversation.advertisement.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not authorized to send payment proposal in this conversation.")
    
    # Create the payment proposal
    return create_payment_proposal(db, request, conversation_id, current_user.id)

@router.get("/{conversation_id}/messages")
def get_conversation_messages(conversation_id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    conversation = db.query(DbConversation).filter(DbConversation.id == conversation_id).first()

    messages = get_messages_for_conversation(db, conversation_id)
    payment_proposals = get_conversation_payment_proposals(db, conversation_id)

    message_displays = [MessageDisplay.model_validate(message) for message in messages]
    payment_proposal_displays = [PaymentProposalDisplay.model_validate(proposal) for proposal in payment_proposals]
    
    return {"messages": message_displays, "payment_proposals": payment_proposal_displays}



