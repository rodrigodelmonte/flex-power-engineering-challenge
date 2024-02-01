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
