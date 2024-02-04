from typing import Optional

from sqlmodel import Field, SQLModel


class Trade(SQLModel, table=True):
    id: str = Field(default=None, nullable=False, primary_key=True)
    price: int
    quantity: int
    direction: str
    delivery_day: str
    delivery_hour: int
    trader_id: str
    execution_time: str


class PnlReports(SQLModel, table=True):
    __tablename__ = "pnl_reports"
    id: str = Field(primary_key=True)
    delivery_hour: Optional[int] = Field(default=None)
    delivery_day: Optional[str] = Field(default=None, index=True)
    number_of_trades: Optional[int] = Field(default=None)
    total_quantity_sold: Optional[int] = Field(default=None)
    total_quantity_bought: Optional[int] = Field(default=None)
    pnl: Optional[int] = Field(default=None)
    total_pnl_for_the_day: Optional[float] = Field(default=None)
