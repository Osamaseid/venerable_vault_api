from sqlalchemy.orm import Session
from . import models, schemas, valuation

def create_item(db: Session, item: schemas.ItemCreate):
    db_item = models.Item(**item.model_dump())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()

def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()

def add_provenance(db: Session, item_id: int, event: schemas.ProvenanceEventCreate):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        return None
    
    db_event = models.ProvenanceEvent(**event.model_dump(), item_id=item_id)
    db.add(db_event)
    
    item.documents_count += 1
    item.updated_at = models.Item.updated_at
    
    db.commit()
    db.refresh(db_event)
    return db_event

def get_provenance_events(db: Session, item_id: int):
    return db.query(models.ProvenanceEvent).filter(models.ProvenanceEvent.item_id == item_id).all()

def create_valuation(db: Session, item_id: int, calculated_value: float, multiplier: float, notes: str = None):
    valuation = models.Valuation(
        calculated_value=calculated_value,
        multiplier_used=multiplier,
        notes=notes,
        item_id=item_id
    )
    db.add(valuation)
    db.commit()
    db.refresh(valuation)
    return valuation

def get_valuations(db: Session, item_id: int):
    return db.query(models.Valuation).filter(models.Valuation.item_id == item_id).all()

def calculate_value(base_cost: float, age_category: str, documents_count: int):
    return valuation.calculate_value(base_cost, age_category, documents_count)