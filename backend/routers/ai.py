from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Optional, Dict, Any

from services.llm import explain_results
from services.dialog import DialogState
from services.dialog_logic import next_question
from services.dialog_store import get_dialog, reset_dialog

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
    session_id: str
    answer: Optional[dict] = None
    results: Optional[List[SearchResult]] = None
    reset: Optional[bool] = False



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
    # 1. reset диалога (если пользователь начал заново)
    if req.reset:
        reset_dialog(req.session_id)

    # 2. получаем состояние
    state = get_dialog(req.session_id)

    # 3. обновляем состояние
    if req.answer:
        state.update(req.answer)

    # 4. следующий шаг
    step = next_question(state)

    if step["type"] == "question":
        return step

    # 5. финал
    if req.results:
        text = explain_results(
            results=[r.dict() for r in req.results],
            user_goal=state.goal,
        )

        return {
            "type": "final",
            "text": text,
            "state": {
                "goal": state.goal,
                "priority": state.priority,
            },
        }

    return {
        "type": "final",
        "text": "Спасибо! Я учёл твои ответы.",
        "state": {
            "goal": state.goal,
            "priority": state.priority,
        },
    }
