from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from services.llm import explain_results
from services.dialog import DialogState
from services.dialog_logic import next_question

router = APIRouter(prefix="/ai", tags=["AI"])

# ------------------------------------------------------------------
# MODELS
# ------------------------------------------------------------------

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


class DialogRequest(BaseModel):
    answer: Optional[Dict[str, Any]] = None
    results: Optional[List[SearchResult]] = None


# ------------------------------------------------------------------
# STATE (временно один диалог на сервер)
# ------------------------------------------------------------------

dialog_state = DialogState()


# ------------------------------------------------------------------
# BASE AI — EXPLAIN (stateless)
# ------------------------------------------------------------------

@router.post("/explain")
def explain_search(data: ExplainRequest):
    if not data.results:
        return {
            "text": (
                "По заданным параметрам ничего не найдено. "
                "Попробуйте изменить фильтры."
            )
        }

    text = explain_results(
        results=[r.dict() for r in data.results],
        user_goal=data.user_goal,
    )

    return {"text": text}


# ------------------------------------------------------------------
# DIALOG AI — WITH CLARIFYING QUESTIONS
# ------------------------------------------------------------------

@router.post("/dialog")
def dialog(req: DialogRequest):
    # 1. Обновляем состояние диалога
    if req.answer:
        dialog_state.update(req.answer)

    # 2. Проверяем, нужен ли ещё вопрос
    step = next_question(dialog_state)

    if step["type"] == "question":
        return step

    # 3. Диалог завершён → объясняем результаты
    if req.results:
        text = explain_results(
            results=[r.dict() for r in req.results],
            user_goal=dialog_state.goal,
        )

        return {
            "type": "final",
            "text": text,
            "state": {
                "goal": dialog_state.goal,
                "priority": dialog_state.priority,
            },
        }

    # 4. Резервный финал
    return {
        "type": "final",
        "text": "Спасибо! Я учёл твои ответы.",
        "state": {
            "goal": dialog_state.goal,
            "priority": dialog_state.priority,
        },
    }
