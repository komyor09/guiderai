from fastapi import FastAPI
from routers import test_db, search


app = FastAPI(title="GuiderAI")

app.include_router(test_db.router)
app.include_router(search.router)

@app.get("/")
def root():
    return {"status": "ok"}