from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.institution import Institution

router = APIRouter(prefix="/test")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/institutions")
def test_institutions(db: Session = Depends(get_db)):
    return db.query(Institution).limit(5).all()
