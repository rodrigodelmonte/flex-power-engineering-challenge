import logging

from fastapi import Depends, FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic_core import ValidationError

from flexpower.api import health, trade
from flexpower.auth import verify_credentials
from flexpower.db import create_db_and_tables

log = logging.getLogger("uvicorn")


def create_application() -> FastAPI:
    application = FastAPI()
    application.include_router(health.router, tags=["health"])
    application.include_router(
        trade.v1,
        tags=["trade"],
        dependencies=[Depends(verify_credentials)],
    )
    return application


app = create_application()


@app.exception_handler(ValidationError)
async def pydantic_core_validation_exception_handler(request: Request, exc: ValidationError):
    errors = [
        {
            "field": e["loc"][0],
            "field_type": e["type"],
            "error_message": e["msg"],
        }
        for e in exc.errors()
    ]
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"status_code": status.HTTP_422_UNPROCESSABLE_ENTITY, "message": errors},
    )


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


@app.on_event("shutdown")
async def shutdown_event():
    log.info("Shutting down...")
