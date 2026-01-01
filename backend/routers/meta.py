from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import SessionLocal
from models.region import Region
from models.district import District
from models.locality import Locality

router = APIRouter(prefix="/meta", tags=["Meta"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# --------------------
# РЕГИОНЫ
# --------------------
@router.get("/regions")
def get_regions(db: Session = Depends(get_db)):
    regions = (
        db.query(Region.id, Region.name, Region.type)
        .order_by(Region.name)
        .all()
    )
    return [dict(r._mapping) for r in regions]


# --------------------
# РАЙОНЫ
# --------------------
@router.get("/districts")
def get_districts(
    region_id: int = Query(..., description="ID региона"),
    db: Session = Depends(get_db),
):
    districts = (
        db.query(District.id, District.name, District.type)
        .filter(District.region_id == region_id)
        .order_by(District.name)
        .all()
    )
    return [dict(d._mapping) for d in districts]


# --------------------
# НАСЕЛЁННЫЕ ПУНКТЫ
# --------------------
@router.get("/localities")
def get_localities(
    district_id: int = Query(..., description="ID района"),
    db: Session = Depends(get_db),
):
    localities = (
        db.query(Locality.id, Locality.name, Locality.type)
        .filter(Locality.district_id == district_id)
        .order_by(Locality.name)
        .all()
    )
    return [dict(l._mapping) for l in localities]
