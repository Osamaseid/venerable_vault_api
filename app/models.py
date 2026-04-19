from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    base_cost = Column(Float, nullable=False)
    age_category = Column(String, nullable=False)
    documents_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    provenance_events = relationship("ProvenanceEvent", back_populates="item", cascade="all, delete-orphan")
    valuations = relationship("Valuation", back_populates="item", cascade="all, delete-orphan")

class ProvenanceEvent(Base):
    __tablename__ = "provenance_events"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    event_type = Column(String, default="restoration")
    documented = Column(Boolean, default=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    item = relationship("Item", back_populates="provenance_events")

class Valuation(Base):
    __tablename__ = "valuations"

    id = Column(Integer, primary_key=True, index=True)
    calculated_value = Column(Float, nullable=False)
    multiplier_used = Column(Float, nullable=False)
    notes = Column(String)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    item = relationship("Item", back_populates="valuations")