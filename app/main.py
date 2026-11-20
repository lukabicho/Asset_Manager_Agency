from fastapi import FastAPI, Request, status
from starlette.responses import JSONResponse

from app.api.v1.endpoints import auth, agency
from app.core.exceptions import AgencyNotFoundError

app = FastAPI(title="Asset Manager API")

@app.get("/health")
def health():
    return {"status": "ok"}

app.include_router(auth.router, prefix="/api/v1")
app.include_router(agency.router, prefix="/api/v1")

@app.exception_handler(AgencyNotFoundError)
def not_found_error(request: Request, exception: AgencyNotFoundError):
    return JSONResponse(status_code=status.HTTP_404_NOT_FOUND, content={"detail": str(exception)})