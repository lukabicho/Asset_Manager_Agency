from fastapi import FastAPI

from app.api.v1.endpoints import auth

app = FastAPI(title="Asset Manager API")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(auth.router, prefix="/api/v1")