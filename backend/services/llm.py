import os
from dotenv import load_dotenv

load_dotenv()

# ---------- PRIMARY (OpenAI) ----------
try:
    from openai import OpenAI
    OPENAI_KEY = os.getenv("OPENAI_API_KEY")

    openai_client = OpenAI(api_key=OPENAI_KEY) if OPENAI_KEY else None
except Exception:
    openai_client = None


# ---------- FALLBACK (g4f) ----------
try:
    import g4f
except Exception:
    g4f = None


def build_context(results: list, user_goal: str | None = None) -> str:
    context = "Вот результаты подбора специальностей:\n\n"

    for r in results[:5]:
        price_text = "бюджет" if r["price"] is None else f"цена {r['price']}"
        context += (
            f"- {r['specialty']} в {r['institution']} ({r['region']}), "
            f"{price_text}, {r['plan_count']} мест\n"
        )

    if user_goal:
        context += f"\nЦель абитуриента: {user_goal}\n"

    context += (
        "\nОбъясни результаты простым языком и помоги сделать выбор."
    )

    return context


def explain_with_openai(prompt: str) -> str:
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "Ты спокойный и умный консультант по выбору специальности. "
                    "Объясняй кратко, по делу, без воды."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.4,
        max_tokens=400,
    )

    return response.choices[0].message.content


def explain_with_g4f(prompt: str) -> str:
    return g4f.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "Ты консультант по выбору специальности."},
            {"role": "user", "content": prompt},
        ],
    )


def explain_results(results: list, user_goal: str | None = None) -> str:
    prompt = build_context(results, user_goal)

    # ---------- TRY OPENAI ----------
    if openai_client:
        try:
            return explain_with_openai(prompt)
        except Exception as e:
            print("OpenAI failed, fallback to g4f:", e)

    # ---------- FALLBACK ----------
    if g4f:
        try:
            return explain_with_g4f(prompt)
        except Exception as e:
            print("g4f failed:", e)

    # ---------- LAST RESORT ----------
    return (
        "Я нашёл несколько вариантов обучения, но сейчас не могу "
        "подробно их объяснить. Попробуйте чуть позже."
    )
