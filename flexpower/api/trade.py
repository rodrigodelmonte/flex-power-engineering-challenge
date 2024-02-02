from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

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


@v1.get("/trades", response_model=List[Trade], status_code=200)
async def get_trade(
    trade_id: Optional[str] = None,
    delivery_day: Optional[str] = None,
    db_session: Session = Depends(get_session),
):

    if delivery_day:
        statement = select(Trade).where(Trade.delivery_day == delivery_day)
    elif trade_id:
        statement = select(Trade).where(Trade.trader_id == trade_id)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="provide trade_id or delivery_day as query parameter",
        )

    trade = db_session.exec(statement).all()
    if not trade:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="not found")
    return trade
