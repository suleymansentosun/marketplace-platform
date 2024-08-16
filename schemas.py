from pydantic import BaseModel
from enum import Enum

class ConditionEnum(str, Enum):
    new = "new"
    refurbished = "refurbished"
    used = "used"

class DeliveryEnum(str, Enum):
    pickup = "pickup"
    send = "send"

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