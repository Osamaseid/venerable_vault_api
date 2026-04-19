from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import SessionLocal
from .. import crud, schemas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/items/", response_model=schemas.ItemResponse)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    return crud.create_item(db, item)

@router.get("/items/", response_model=List[schemas.ItemResponse])
def list_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_items(db, skip, limit)

@router.get("/items/{item_id}", response_model=schemas.ItemResponse)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.post("/items/{item_id}/provenance/", response_model=schemas.ProvenanceEventResponse)
def add_provenance(item_id: int, event: schemas.ProvenanceEventCreate, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return crud.add_provenance(db, item_id, event)

@router.get("/items/{item_id}/provenance/", response_model=List[schemas.ProvenanceEventResponse])
def get_provenance(item_id: int, db: Session = Depends(get_db)):
    return crud.get_provenance_events(db, item_id)

@router.get("/items/{item_id}/valuation/", response_model=schemas.ValuationResult)
def get_valuation(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    value, multiplier = crud.calculate_value(item.base_cost, item.age_category, item.documents_count)
    
    return {
        "item_id": item.id,
        "item_name": item.name,
        "base_cost": item.base_cost,
        "age_category": item.age_category,
        "provenance_events_count": len(item.provenance_events),
        "valuation": value,
        "multiplier_used": multiplier
    }

@router.get("/items/{item_id}/valuations/", response_model=List[schemas.ValuationResponse])
def get_valuation_history(item_id: int, db: Session = Depends(get_db)):
    return crud.get_valuations(db, item_id)