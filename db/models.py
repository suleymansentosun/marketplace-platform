from sqlalchemy.sql.sqltypes import Integer, String, Boolean
from db.database import Base
from sqlalchemy import Column, DateTime, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum
from sqlalchemy.sql import func

class ConditionEnum(str, Enum):
    new = "new"
    refurbished = "refurbished"
    used = "used"

class DeliveryEnum(str, Enum):
    pickup = "pickup"
    send = "send"

class TransactionStatusEnum(str, Enum):
    proposal_sended = "proposal_sended"
    proposal_rejected = "proposal_rejected"
    payment_done = "payment_done"

class DbCategory(Base):
    __tablename__ = 'categories'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True)
    advertisements = relationship("DbAdvertisement", back_populates="category")

class DbAdvertisement(Base):
    __tablename__= "advertisements"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    price = Column(Integer)
    description = Column(String)
    condition = Column(SQLAlchemyEnum(ConditionEnum))
    delivery = Column(SQLAlchemyEnum(DeliveryEnum))
    category_id = Column(Integer, ForeignKey('categories.id'))
    category = relationship("DbCategory", back_populates="advertisements")
    conversations = relationship("DbConversation", back_populates="advertisement")
    seller_id = Column(Integer, ForeignKey('users.id'))
    # created_time = Column(DateTime)

class DbTransaction(Base):
    __tablename__= "transactions"
    id = Column(Integer, primary_key=True, index=True)
    payment_amount = Column(Integer)
    status = Column(SQLAlchemyEnum(TransactionStatusEnum), default=TransactionStatusEnum.proposal_sended)

class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)

class DbConversation(Base):
    __tablename__ = 'conversations'
    id = Column(Integer, primary_key=True, index=True)
    advertisement_id = Column(Integer, ForeignKey('advertisements.id'), nullable=False)
    buyer_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    advertisement = relationship("DbAdvertisement", back_populates="conversations")
    messages = relationship("DbMessage", back_populates="conversation", cascade="all, delete-orphan")

class DbMessage(Base):
    __tablename__ = 'messages'
    id = Column(Integer, primary_key=True, index=True)
    conversation_id = Column(Integer, ForeignKey('conversations.id'), nullable=False)
    content = Column(String, nullable=False)
    is_from_seller = Column(Boolean, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    conversation = relationship("Conversation", back_populates="messages")


