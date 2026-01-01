def next_question(state):
    if state.goal is None:
        return {
            "type": "question",
            "key": "goal",
            "text": "Что для тебя важнее при поступлении?",
            "options": [
                {"value": "budget", "label": "Бюджет (бесплатно)"},
                {"value": "prestige", "label": "Престиж вуза"},
                {"value": "doesnt_matter", "label": "Без разницы"}
            ]
        }

    if state.priority is None:
        return {
            "type": "question",
            "key": "priority",
            "text": "На что сделать упор при подборе?",
            "options": [
                {"value": "price", "label": "Цена обучения"},
                {"value": "region", "label": "Регион"},
                {"value": "specialty", "label": "Специальность"}
            ]
        }

    return {"type": "complete"}
