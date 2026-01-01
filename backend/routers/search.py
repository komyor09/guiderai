from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from database import SessionLocal

from models.admission_plan import AdmissionPlan
from models.institution import Institution
from models.specialty import Specialty
from models.language import Language
from models.admission_plan_language import AdmissionPlanLanguage

from models.region import Region
from models.district import District
from models.locality import Locality

router = APIRouter(prefix="/search", tags=["Search"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def search(
    language: str | None = Query(None),
    specialty: str | None = Query(None),
    budget: bool | None = Query(None),

    region_id: int | None = Query(None),
    district_id: int | None = Query(None),
    locality_id: int | None = Query(None),

    sort: str | None = Query(
        None, description="price | plan_count | institution"
    ),
    order: str = Query(
        "desc", description="asc | desc"
    ),
    limit: int = Query(
        20, ge=1, le=100
    ),

    db: Session = Depends(get_db),
):

    query = (
        db.query(
            Institution.name.label("institution"),
            Region.name.label("region"),
            Specialty.name.label("specialty"),
            Language.name.label("language"),
            AdmissionPlan.price,
            AdmissionPlan.plan_count,
        )
        .select_from(AdmissionPlan)
        .join(Institution, Institution.id == AdmissionPlan.institution_id)
        .join(Specialty, Specialty.id == AdmissionPlan.specialty_id)
        .join(AdmissionPlanLanguage, AdmissionPlanLanguage.admission_plan_id == AdmissionPlan.id)
        .join(Language, Language.id == AdmissionPlanLanguage.language_id)
        .join(Locality, Locality.id == Institution.locality_id)
        .join(District, District.id == Locality.district_id)
        .join(Region, Region.id == District.region_id)
    )

    # ---------- ФИЛЬТРЫ ----------

    if language:
        query = query.filter(Language.name.ilike(f"%{language}%"))

    if specialty:
        query = query.filter(Specialty.name.ilike(f"%{specialty}%"))

    if budget is not None:
        query = query.filter(
            AdmissionPlan.price.is_(None)
            if budget
            else AdmissionPlan.price.isnot(None)
        )

    # География (ПО ID, ВАЖНО!)
    if locality_id:
        query = query.filter(Locality.id == locality_id)
    elif district_id:
        query = query.filter(District.id == district_id)
    elif region_id:
        query = query.filter(Region.id == region_id)

        # ---------- СОРТИРОВКА ----------

    if sort == "price":
        column = AdmissionPlan.price
    elif sort == "plan_count":
        column = AdmissionPlan.plan_count
    elif sort == "institution":
        column = Institution.name
    else:
        column = None

    if column is not None:
        query = query.order_by(
            column.asc() if order == "asc" else column.desc()
        )

    results = query.limit(limit).all()
    return [dict(r._mapping) for r in results]

    results = query.limit(20).all()
    return [dict(r._mapping) for r in results]
