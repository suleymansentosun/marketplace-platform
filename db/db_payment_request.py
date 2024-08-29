from sqlalchemy import desc
from sqlalchemy.orm.session import Session
from db.models import DbPaymentProposal
from schemas import PaymentProposalCreate

def create_payment_proposal(db: Session, request: PaymentProposalCreate, conversation_id, sender_id):
    new_proposal = DbPaymentProposal(
        conversation_id = conversation_id,
        sender_id = sender_id,
        amount = request.amount,
        delivery_detail = request.delivery_detail,
        status = "pending"
    )
    db.add(new_proposal)
    db.commit()
    db.refresh(new_proposal)
    return new_proposal

def get_conversation_payment_proposals(db: Session, conversation_id: int):
    return db.query(DbPaymentProposal).filter(DbPaymentProposal.conversation_id == conversation_id).all()

def get_last_payment_request_in_specific_conversation(db: Session, conversation_id: int):
  return db.query(DbPaymentProposal).filter(DbPaymentProposal.conversation_id == conversation_id).order_by(
            desc(DbPaymentProposal.created_at)).first()
