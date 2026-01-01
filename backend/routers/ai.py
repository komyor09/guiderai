from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional

from services.llm import explain_results

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
    user_goal: Optional[str] = None


@router.post("/explain")
def explain_search(data: ExplainRequest):
    if not data.results:
        return {
            "text": "По заданным параметрам ничего не найдено. "
                    "Попробуйте изменить фильтры."
        }

    text = explain_results(
        results=[r.dict() for r in data.results],
        user_goal=data.user_goal,
    )

    return {"text": text}
