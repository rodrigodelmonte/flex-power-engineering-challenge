import logging

from fastapi import FastAPI

from flexpower.api import health, trade
from flexpower.db import create_db_and_tables

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(health.router, tags=["health"])
    application.include_router(trade.v1, tags=["trade"])
    return application


app = create_application()


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
