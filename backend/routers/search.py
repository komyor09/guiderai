from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from database import SessionLocal
from models.admission_plan import AdmissionPlan
from models.institution import Institution
from models.specialty import Specialty
from models.language import Language
from models.admission_plan_language import AdmissionPlanLanguage

router = APIRouter(prefix="/search")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def search(
    language: str | None = Query(None),
    budget: bool | None = Query(None),
    region: str | None = Query(None),
    specialty: str | None = Query(None),
    db: Session = Depends(get_db)
):
    q = (
        db.query(
            Institution.name.label("institution"),
            Institution.region,
            Specialty.name.label("specialty"),
            Language.name.label("language"),
            AdmissionPlan.price,
            AdmissionPlan.plan_count,
        )
        .join(AdmissionPlan, AdmissionPlan.institution_id == Institution.id)
        .join(Specialty, Specialty.id == AdmissionPlan.specialty_id)
        .join(AdmissionPlanLanguage, AdmissionPlanLanguage.admission_plan_id == AdmissionPlan.id)
        .join(Language, Language.id == AdmissionPlanLanguage.language_id)
    )
    if language:
        q = q.filter(Language.name.ilike(f"%{language}%"))

    if budget is not None:
        if budget:
            q = q.filter(AdmissionPlan.price.is_(None))
        else:
            q = q.filter(AdmissionPlan.price.isnot(None))

    if region:
        q = q.filter(Institution.region.ilike(f"%{region}%"))

    if specialty:
        q = q.filter(Specialty.name.ilike(f"%{specialty}%"))

    results = q.limit(20).all()
    return [dict(row._mapping) for row in results]