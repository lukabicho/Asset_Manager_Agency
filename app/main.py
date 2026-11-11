from fastapi import FastAPI

app = FastAPI(title="Asset Manager API")

@app.get("/health")
def health():
    return {"status": "ok"}