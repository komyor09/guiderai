from fastapi import FastAPI
from routers import test_db

app = FastAPI(title="GuiderAI")

app.include_router(test_db.router)

@app.get("/")
def root():
    return {"status": "ok"}

