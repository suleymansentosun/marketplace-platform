from datetime import datetime
from typing import List, Optional, Text
from pydantic import BaseModel
from enum import Enum

class ConditionEnum(str, Enum):
    new = "new"
    refurbished = "refurbished"
    used = "used"

class DeliveryTypeEnum(str, Enum):
    pickup = "pickup"
    send = "send"

class PaymentProposalStatusEnum(str, Enum):
    pending = "pending"
    confirmed = "confirmed"

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
    delivery: DeliveryTypeEnum
    category_id: int
    owner_id: int

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
    delivery: DeliveryTypeEnum
    category_id: int
    owner_id: int
    class Config():
        from_attributes = True

class PaymentProposalCreate(BaseModel):
    amount: int
    delivery_detail: DeliveryTypeEnum

class PaymentProposalDisplay(BaseModel):
    id: int
    conversation_id: int
    sender_id: int
    amount: int
    delivery_detail: DeliveryTypeEnum
    status: PaymentProposalStatusEnum
    created_at: datetime
    class Config():
        from_attributes = True
        

class UserBase(BaseModel):
    username: str
    email: str
    password: str

class UserDisplay(BaseModel):
    id: int
    username: str
    email: str 
    avarage_rating: Optional [float]
    class Config():
        from_attributes = True
        
class UserAllDisplay(BaseModel):
    id: int
    username: str
    email: str 
    avarage_rating: Optional [float]
    class Config():
        from_attributes = True

class MessageBase(BaseModel):
    content: str
    sender_user_id: int
    advertisement_id: int
    buyer_user_id: int

class MessageDisplay(BaseModel):
    id: int
    content: str
    sender_user_id: int
    created_at: datetime
    class Config:
        from_attributes = True

class ConversationSpecificDisplay(BaseModel):
    id: int
    advertisement_id: int
    buyer_id: int
    seller_id: int
    messages: List[MessageDisplay] = []
    payment_proposals: List[PaymentProposalDisplay] = []
    class Config:
        orm_mode = True

class ConversationListDisplay(BaseModel):
    advertisement_title: str
    last_message_content: str  
    last_message_owner: int  
    last_message_date: datetime
    transaction_status: Optional[str] = None

    class Config:
        orm_mode = True
        
class ReviewBase(BaseModel):
    reviewer_id: int
    reviewed_user_id: int
    rating: float
    review_content: str
        
class ReviewDisplay(BaseModel):
    id : int
    rating : float
    review_content : Text

class ReviewUpdateDisplay(BaseModel):
    rating : float
    review_content : Text
        