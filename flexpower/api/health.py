from fastapi import APIRouter, Depends

from flexpower.config import Settings, get_settings

router = APIRouter()


@router.get("/health")
async def health(settings: Settings = Depends(get_settings)):
    return {
        "environment": settings.environment,
        "health": True,
        "testing": settings.testing,
    }
