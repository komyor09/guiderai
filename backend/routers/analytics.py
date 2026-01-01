from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func

from database import SessionLocal
from models.search_log import SearchLog

router = APIRouter(prefix="/analytics", tags=["Analytics"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/overview")
def overview(db: Session = Depends(get_db)):
    total = db.query(func.count(SearchLog.id)).scalar()

    top_regions = (
        db.query(SearchLog.region_id, func.count().label("count"))
        .filter(SearchLog.region_id.isnot(None))
        .group_by(SearchLog.region_id)
        .order_by(func.count().desc())
        .limit(5)
        .all()
    )

    top_specialties = (
        db.query(SearchLog.specialty, func.count().label("count"))
        .filter(SearchLog.specialty.isnot(None))
        .group_by(SearchLog.specialty)
        .order_by(func.count().desc())
        .limit(5)
        .all()
    )

    return {
        "total_searches": total,
        "top_regions": [
            {"region_id": r.region_id, "count": r.count} for r in top_regions
        ],
        "top_specialties": [
            {"specialty": s.specialty, "count": s.count} for s in top_specialties
        ],
    }
