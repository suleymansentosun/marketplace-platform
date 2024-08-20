from sqlalchemy.sql.sqltypes import Integer, String
from db.database import Base
from sqlalchemy import Column, DateTime, Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import relationship
from enum import Enum

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
    # created_time = Column(DateTime)
    transaction = relationship('DbTransaction', back_populates='advertisement', uselist=False)

class DbTransaction(Base):
    __tablename__= "transactions"
    id = Column(Integer, primary_key=True, index=True)
    payment_amount = Column(Integer)
    status = Column(SQLAlchemyEnum(TransactionStatusEnum), default=TransactionStatusEnum.proposal_sended)
    advertisement_id = Column(Integer, ForeignKey('advertisements.id'), nullable=False)
    advertisement = relationship('DbAdvertisement', back_populates='transaction')


