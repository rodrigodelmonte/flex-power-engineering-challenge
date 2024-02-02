from fastapi import APIRouter, Depends
from sqlmodel import Session

from flexpower.db import get_session
from flexpower.models.trade import Trade

v1 = APIRouter(prefix="/v1")


@v1.post("/trades", response_model=None, status_code=201)
async def add_trade(
    trade: Trade,
    db_session: Session = Depends(get_session),
):
    validated_trade = Trade.model_validate(trade)
    db_session.add(validated_trade)
    db_session.commit()
