import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def explain_results(results: list, user_goal: str | None = None) -> str:
    """
    results — список словарей из /search
    user_goal — цель пользователя (опционально)
    """

    system_prompt = (
        "Ты — умный и спокойный консультант по выбору специальности. "
        "Говори просто, по делу, без лишней воды. "
        "Объясняй, помогай сравнивать, задавай уточняющие вопросы."
    )

    context = "Вот результаты поиска:\n"
    for r in results[:5]:
        price_text = "бюджет" if r["price"] is None else f"цена {r['price']}"

        context += (
            f"- {r['specialty']} в {r['institution']} ({r['region']}), "
            f"{price_text}, {r['plan_count']} мест\n"
        )

    if user_goal:
        context += f"\nЦель пользователя: {user_goal}\n"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": context},
        ],
        temperature=0.4,
        max_tokens=400,
    )

    return response.choices[0].message.content
