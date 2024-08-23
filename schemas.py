from datetime import datetime
from typing import List, Text
from pydantic import BaseModel
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

class CategoryBase(BaseModel):
    name: str

class CategoryDisplay(BaseModel):
    name: str
    class Config:
        orm_mode = True

class AdvertisementBase(BaseModel):
    title: str
    price: int
    description: str
    condition: ConditionEnum
    delivery: DeliveryEnum
    category_id: int

class AdvertisementListDisplay(BaseModel):
    title: str
    price: int
    class Config():
        from_attributes = True

class AdvertisementDetailDisplay(BaseModel):
    title: str
    price: int
    description: str
    condition: ConditionEnum
    delivery: DeliveryEnum
    category_id: int
    class Config():
        from_attributes = True

class TransactionBase(BaseModel):
    payment_amount: int
    advertisement_id: int

class TransactionDisplay(BaseModel):
    id: int
    payment_amount: int
    status: TransactionStatusEnum
    advertisement_id: int
    class Config:
        orm_mode = True
        

class UserBase(BaseModel):
    #id: int
    username: str
    email: str
    password: str

class UserDisplay(BaseModel):
    id: int
    username: str
    email: str 
    class Config():
        from_attributes = True

# class MessageBase(BaseModel):
#     content: str,
    

class MessageDisplay(MessageBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class ConversationBase(BaseModel):
    advertisement_id: int
    buyer_id: int

class ConversationDisplay(ConversationBase):
    id: int
    seller_id: int
    messages: List[MessageDisplay] = []
    class Config:
        orm_mode = True
        
class ReviewBase(BaseModel):
    reviewer_id : int
    reviewed_user_id : int
    rating : float
    review_content : Text
        
class ReviewDisplay(BaseModel):
    id : int
    rating : float
    review_content : Text
        