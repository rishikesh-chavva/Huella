from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
import models, schemas
from auth import get_current_user

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/summary", response_model=schemas.DashboardSummary)
def get_summary(
    current_user: models.User = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    passports = db.query(models.Passport).filter(models.Passport.user_id == current_user.id).all()
    
    total_products = len(passports)
    total_co2 = sum(p.carbon_footprint for p in passports)
    avg_co2 = total_co2 / total_products if total_products > 0 else 0
    
    return {
        "total_products": total_products,
        "average_co2": round(avg_co2, 2),
        "total_co2_tracked": round(total_co2, 2)
    }
