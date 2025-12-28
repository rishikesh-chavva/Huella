from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session
from auth import get_current_user
from database import get_db
import models, schemas
from ai.document_intelligence import analyze_invoice
from ai.carbon_calc import calculate_footprint

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # 1. Read file content
    content = await file.read()
    
    # 2. Extract data via Azure AI
    extraction = await analyze_invoice(content)
    
    # 3. Process items and create Passports
    created_passports = []
    
    if not extraction["items"]:
        raise HTTPException(status_code=400, detail="No items detected in document.")

    for item in extraction["items"]:
        material = item["description"]
        quantity = item["quantity"] if item["quantity"] > 0 else 1.0 # Default fallback
        origin = extraction["location"]
        
        # Calculate CO2
        co2 = calculate_footprint(material, quantity)
        
        # Save to DB
        new_passport = models.Passport(
            product_name=f"{material} Product",
            material=material,
            quantity=quantity,
            origin=origin,
            carbon_footprint=co2,
            user_id=current_user.id
        )
        db.add(new_passport)
        created_passports.append(new_passport)
    
    db.commit()
    
    return {
        "message": f"Successfully processed {len(created_passports)} items",
        "vendor": extraction["vendor"],
        "extracted_data": extraction["items"]
    }
