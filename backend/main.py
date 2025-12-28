from fastapi import FastAPI

app = FastAPI(title="GuiderAI")

@app.get("/")
def root():
    return {"status": "ok"}
