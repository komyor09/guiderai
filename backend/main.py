from fastapi import FastAPI
from routers import test_db, search, meta, analytics, ai
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="GuiderAI")


app.include_router(test_db.router)
app.include_router(analytics.router)
app.include_router(ai.router)
app.include_router(meta.router)
app.include_router(search.router)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"status": "ok"}