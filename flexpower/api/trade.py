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
    trade = Trade(
        id=trade.id,
        price=trade.price,
        quantity=trade.quantity,
        direction=trade.direction,
        delivery_day=trade.delivery_day,
        delivery_hour=trade.delivery_hour,
        trader_id=trade.trader_id,
        execution_time=trade.execution_time,
    )
    db_trade = Trade.model_validate(trade)
    db_session.add(db_trade)
    db_session.commit()
