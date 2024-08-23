from sqlalchemy.sql.sqltypes import Integer, String, Float, Text
from db.database import Base
from sqlalchemy import Column, DateTime, Enum as SQLAlchemyEnum, ForeignKey 
from sqlalchemy.orm import relationship, validates
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

class DbUser(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    reviews_given = relationship('DbReview', foreign_keys='DbReview.reviewer_id', back_populates='reviewer') 
    reviews_received = relationship("DbReview", foreign_keys='DbReview.reviewed_user_id', back_populates='reviewed_user')

class DbReview(Base):
    __tablename__ = 'reviews'
    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Float, nullable=False)
    review_content = Column(Text)
    reviewer_id = Column(Integer, ForeignKey('users.id'))
    reviewed_user_id = Column(Integer, ForeignKey('users.id'))
    reviewer = relationship('DbUser', back_populates='reviews_given', foreign_keys=[reviewer_id])     
    reviewed_user = relationship('DbUser', back_populates='reviews_received', foreign_keys=[reviewed_user_id])
    
    @validates('rating')
    def validate_rating(self, key, value):
        #if value < 1 or value > 5:
        #   raise ValueError("Please rate the user between 1 and 5 stars")
        assert value >= 1 or value <= 5
        return value


