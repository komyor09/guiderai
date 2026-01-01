from typing import Optional, Dict


class DialogState:
    def __init__(self):
        self.goal: Optional[str] = None        # бюджет / престиж / всё равно
        self.priority: Optional[str] = None    # цена / регион / специальность

    def update(self, data: Dict):
        if "goal" in data:
            self.goal = data["goal"]
        if "priority" in data:
            self.priority = data["priority"]

    def is_complete(self) -> bool:
        return self.goal is not None and self.priority is not None
