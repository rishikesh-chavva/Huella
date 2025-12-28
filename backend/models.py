from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    company = Column(String)
    
    passports = relationship("Passport", back_populates="owner")

class Passport(Base):
    __tablename__ = "passports"

    id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String)
    material = Column(String)
    quantity = Column(Float)  # in kg
    origin = Column(String)
    carbon_footprint = Column(Float) # total kg CO2
    user_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    
    owner = relationship("User", back_populates="passports")
