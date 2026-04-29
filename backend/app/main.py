from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.workers.scheduler import start_scheduler, stop_scheduler

app = FastAPI(title=settings.app_name)
app.include_router(router, prefix=settings.api_prefix)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.on_event("startup")
async def startup_event():
    start_scheduler()


@app.on_event("shutdown")
async def shutdown_event():
    stop_scheduler()
