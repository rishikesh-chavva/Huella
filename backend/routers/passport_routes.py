from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
import models, schemas
from auth import get_current_user

router = APIRouter(prefix="/passports", tags=["Passports"])

@router.get("/", response_model=List[schemas.PassportResponse])
def get_user_passports(
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    return db.query(models.Passport).filter(models.Passport.user_id == current_user.id).all()

@router.get("/{passport_id}", response_model=schemas.PassportResponse)
def get_passport_detail(
    passport_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    passport = db.query(models.Passport).filter(
        models.Passport.id == passport_id,
        models.Passport.user_id == current_user.id
    ).first()
    
    if not passport:
        raise HTTPException(status_code=404, detail="Passport not found")
    return passport

@router.delete("/{passport_id}")
def delete_passport(
    passport_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    passport = db.query(models.Passport).filter(
        models.Passport.id == passport_id,
        models.Passport.user_id == current_user.id
    ).first()
    
    if not passport:
        raise HTTPException(status_code=404, detail="Passport not found")
    
    db.delete(passport)
    db.commit()
    return {"message": "Passport deleted successfully"}
