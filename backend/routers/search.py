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
    language: str | None = Query(None, description="Язык обучения"),
    budget: bool | None = Query(None, description="Бюджет или платно"),
    region: str | None = Query(None, description="Регион (область/город)"),
    specialty: str | None = Query(None, description="Название специальности"),
    db: Session = Depends(get_db),
):
    """
    Основной поиск специальностей.
    Работает через нормализованную географию:
    regions → districts → localities → institutions
    """

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
        # --- Учебные данные ---
        .join(Institution, Institution.id == AdmissionPlan.institution_id)
        .join(Specialty, Specialty.id == AdmissionPlan.specialty_id)
        .join(
            AdmissionPlanLanguage,
            AdmissionPlanLanguage.admission_plan_id == AdmissionPlan.id,
        )
        .join(Language, Language.id == AdmissionPlanLanguage.language_id)
        # --- География ---
        .join(Locality, Locality.id == Institution.locality_id)
        .join(District, District.id == Locality.district_id)
        .join(Region, Region.id == District.region_id)
    )

    # ---------- ФИЛЬТРЫ ----------

    if language:
        query = query.filter(Language.name.ilike(f"%{language}%"))

    if budget is not None:
        query = query.filter(
            AdmissionPlan.price.is_(None)
            if budget
            else AdmissionPlan.price.isnot(None)
        )

    if region:
        query = query.filter(Region.name.ilike(f"%{region}%"))

    if specialty:
        query = query.filter(Specialty.name.ilike(f"%{specialty}%"))

    # ---------- РЕЗУЛЬТАТ ----------

    results = query.limit(20).all()

    return [dict(row._mapping) for row in results]
