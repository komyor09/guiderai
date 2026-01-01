from typing import Dict
from services.dialog import DialogState

# session_id -> DialogState
_dialogs: Dict[str, DialogState] = {}


def get_dialog(session_id: str) -> DialogState:
    if session_id not in _dialogs:
        _dialogs[session_id] = DialogState()
    return _dialogs[session_id]


def reset_dialog(session_id: str):
    _dialogs.pop(session_id, None)
