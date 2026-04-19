from fastapi import FastAPI
from .database import SessionLocal, engine, Base
from .routes import items

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Venerable Vault API",
    description="Antique valuation and provenance tracking system",
    version="1.0.0"
)

app.include_router(items.router, prefix="/api", tags=["items"])

@app.get("/")
def root():
    return {"message": "Venerable Vault API - Antique Valuation System"}

@app.get("/health")
def health():
    return {"status": "healthy"}