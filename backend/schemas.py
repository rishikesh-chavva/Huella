from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    name: str
    company: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

class PassportBase(BaseModel):
    product_name: str
    material: str
    quantity: float
    origin: str

class PassportCreate(PassportBase):
    carbon_footprint: float

class PassportResponse(PassportBase):
    id: int
    carbon_footprint: float
    timestamp: datetime
    user_id: int
    class Config:
        from_attributes = True

class DashboardSummary(BaseModel):
    total_products: int
    average_co2: float
    total_co2_tracked: float
