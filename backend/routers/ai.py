from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/ai", tags=["AI"])


class SearchResult(BaseModel):
    institution: str
    region: str
    specialty: str
    language: str
    price: Optional[int]
    plan_count: int


class ExplainRequest(BaseModel):
    results: List[SearchResult]
    user_goal: Optional[str] = None  # например: "бюджет", "престиж", "рядом с домом"


@router.post("/explain")
def explain_search(data: ExplainRequest):
    """
    Пока без реального LLM — заглушка.
    На следующем шаге подключим модель.
    """

    if not data.results:
        return {
            "text": "По заданным параметрам подходящих вариантов не найдено. "
                    "Попробуйте изменить регион, язык или тип обучения."
        }

    top = data.results[:3]

    explanation = (
        f"Я подобрал {len(data.results)} вариантов обучения. "
        f"Обратите внимание на следующие направления:\n\n"
    )

    for r in top:
        explanation += (
            f"• {r.specialty} в {r.institution} ({r.region}) — "
            f"{'бюджет' if r.price is None else f'стоимость {r.price}'} сомони, "
            f"{r.plan_count} мест.\n"
        )

    explanation += (
        "\nЕсли хочешь, я могу:\n"
        "— сравнить эти варианты между собой;\n"
        "— подобрать самый бюджетный;\n"
        "— найти вариант ближе к дому."
    )

    return {"text": explanation}
