from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth.oauth2 import get_current_user
from db.database import get_db
from db.models import DbPaymentProposal
from schemas import PaymentProposalStatusEnum, UserBase

router = APIRouter(
    prefix="/payment-proposal",
    tags=["payment-proposal"]
)

@router.patch("/{proposal_id}/confirm")
def confirm_payment(proposal_id: int, db: Session = Depends(get_db), current_user: UserBase = Depends(get_current_user)):
    proposal = db.query(DbPaymentProposal).filter(DbPaymentProposal.id == proposal_id).first()
    
    if not proposal:
        raise HTTPException(status_code=404, detail="Payment proposal not found.")
    
    conversation = proposal.conversation
    if (proposal.sender_id == conversation.buyer_id and current_user.id != conversation.advertisement.owner_id) or \
       (proposal.sender_id == conversation.advertisement.owner_id and current_user.id != conversation.buyer_id):
        raise HTTPException(status_code=403, detail="Not authorized to confirm this payment.")

    proposal.status = PaymentProposalStatusEnum.confirmed
    db.commit()
    
    return {"message": "Payment confirmed."}
