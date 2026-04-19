from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List

class ProvenanceEventCreate(BaseModel):
    description: str
    year: int
    event_type: str = "restoration"
    documented: bool = True

class ProvenanceEventResponse(ProvenanceEventCreate):
    id: int
    item_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ItemCreate(BaseModel):
    name: str
    base_cost: float
    age_category: str
    documents_count: int = 0

class ItemResponse(ItemCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    provenance_events: List[ProvenanceEventResponse] = []

    model_config = ConfigDict(from_attributes=True)

class ValuationCreate(BaseModel):
    notes: Optional[str] = None

class ValuationResponse(BaseModel):
    id: int
    calculated_value: float
    multiplier_used: float
    notes: Optional[str]
    item_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

class ValuationResult(BaseModel):
    item_id: int
    item_name: str
    base_cost: float
    age_category: str
    provenance_events_count: int
    valuation: float
    multiplier_used: float