from sqlalchemy.sql.sqltypes import Integer, String, Boolean, Float, Text
from db.database import Base
from sqlalchemy import Column, DateTime, Enum as SQLAlchemyEnum, ForeignKey 
from sqlalchemy.orm import relationship, validates
from enum import Enum
from sqlalchemy.sql import func

class ConditionEnum(str, Enum):
    new = "new"
    refurbished = "refurbished"
    used = "used"

class PaymentProposalStatusEnum(str, Enum):
    pending = "pending"
    confirmed = "confirmed" 

class DeliveryTypeEnum(str, Enum):
    shipping = "shipping"
    pickup = "pickup"

class DbCategory(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True)
    name = Column(String, index=True, unique=True)
    advertisements = relationship("DbAdvertisement", back_populates="category")

class DbAdvertisement(Base):
    __tablename__= "advertisements"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    price = Column(Integer)
    description = Column(String)
    condition = Column(SQLAlchemyEnum(ConditionEnum))
    delivery = Column(SQLAlchemyEnum(DeliveryTypeEnum))
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("DbCategory", back_populates="advertisements")
    conversations = relationship("DbConversation", back_populates="advertisement")
    owner_id = Column(Integer, ForeignKey('users.id'))
    # created_time = Column(DateTime)

<<<<<<< HEAD
# class DbTransaction(Base):
#     __tablename__= "transactions"
#     id = Column(Integer, primary_key=True, index=True)
#     conversation_id = Column(Integer, ForeignKey("conversations.id"))
#     payment_amount = Column(Integer)
#     status = Column(SQLAlchemyEnum(TransactionStatusEnum), default=TransactionStatusEnum.proposal_sended)
#     conversation = relationship("DbConversation", back_populates="transactions")
#     created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

class DbPaymentProposal(Base):
    __tablename__ = "payment_proposals"
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'))
    sender_id = Column(Integer, ForeignKey('users.id'))
    amount = Column(Integer, nullable=False)
    delivery_detail = Column(SQLAlchemyEnum(DeliveryTypeEnum), nullable=False)
    status = Column(SQLAlchemyEnum(PaymentProposalStatusEnum), default=PaymentProposalStatusEnum.pending)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    conversation = relationship("DbConversation", back_populates="payment_proposals")
    sender = relationship("DbUser", back_populates="sent_payment_proposals")

=======
class DbTransaction(Base):
    __tablename__= "transactions"
    id = Column(Integer, primary_key=True)
    payment_amount = Column(Integer)
    status = Column(SQLAlchemyEnum(TransactionStatusEnum), default=TransactionStatusEnum.proposal_sended)
    advertisement_id = Column(Integer, ForeignKey('advertisements.id'), nullable=False)
    advertisement = relationship('DbAdvertisement', back_populates='transaction')
>>>>>>> develop

class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    reviews_given = relationship('DbReview', foreign_keys='DbReview.reviewer_id', back_populates='reviewer') 
    reviews_received = relationship("DbReview", foreign_keys='DbReview.reviewed_user_id', back_populates='reviewed_user')
    messages = relationship("DbMessage", back_populates="sender")
    sent_payment_proposals = relationship("DbPaymentProposal", back_populates="sender")

class DbReview(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True)
    rating = Column(Float, nullable=False)
    review_content = Column(Text)
    reviewer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    reviewed_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    reviewer = relationship('DbUser', back_populates='reviews_given', foreign_keys=[reviewer_id])     
    reviewed_user = relationship('DbUser', back_populates='reviews_received', foreign_keys=[reviewed_user_id])
    
    @validates('rating')
    def validate_rating(self, key, value):
        assert value >= 1 and value <= 5
        return value


class DbConversation(Base):
    __tablename__ = 'conversations'
    id = Column(Integer, primary_key=True, index=True)
    advertisement_id = Column(Integer, ForeignKey('advertisements.id'), nullable=True)
    buyer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    advertisement = relationship("DbAdvertisement", back_populates="conversations")
    messages = relationship("DbMessage", back_populates="conversation", cascade="all, delete-orphan")
    # transactions = relationship("DbTransaction", back_populates="conversation")
    payment_proposals = relationship("DbPaymentProposal", back_populates="conversation")

class DbMessage(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'), nullable=False)
    content = Column(String, nullable=False)
    sender_user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    conversation = relationship("DbConversation", back_populates="messages")
    sender = relationship("DbUser", back_populates="messages")



