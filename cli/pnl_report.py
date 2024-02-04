"""
CLI designed to generate and display a Profit and Loss (PnL) report for a specified date from the pnl_reports table,
which is assumed to exist in the PostgreSQL database.

Example:
export POSTGRES_USER=<your-username>
export POSTGRES_PASSWORD=<your-password>
export POSTGRES_HOST=<your-db-host>
export POSTGRES_DB=<your-database>

python ./pnl_report.py 2024-02-01
"""

import os
from typing import Optional

import typer
from sqlmodel import Field, Session, SQLModel, create_engine, select

postgres_user = os.environ.get("POSTGRES_USER")
postgres_password = os.environ.get("POSTGRES_PASSWORD")
postgres_host = os.environ.get("POSTGRES_HOST")
postgres_db = os.environ.get("POSTGRES_DB")
DATABASE_URL = (
    f"postgresql+psycopg2://{postgres_user}:{postgres_password}@{postgres_host}:5432/{postgres_db}"
)

app = typer.Typer()

engine = create_engine(DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session


class PnlReports(SQLModel, table=True):
    __tablename__ = "pnl_reports"
    id: str = Field(primary_key=True)
    delivery_hour: Optional[int] = Field(default=None)
    delivery_day: Optional[str] = Field(default=None)
    number_of_trades: Optional[int] = Field(default=None)
    total_quantity_sold: Optional[int] = Field(default=None)
    total_quantity_bought: Optional[int] = Field(default=None)
    pnl: Optional[int] = Field(default=None)
    total_pnl_for_the_day: Optional[float] = Field(default=None)


@app.command()
def pnl_report(date: str):
    with Session(engine) as session:  # Correct usage of session
        statement = select(PnlReports).where(PnlReports.delivery_day == date)
        results = session.exec(statement).all()
        typer.echo("HOUR\tNun. Trades\tTotal BUY [MW]\tTotal Sell [MW]\tPnL [Eur]")
        for res in results:
            typer.echo(
                f"{res.delivery_hour}\t{res.number_of_trades}\t\t{res.total_quantity_bought}\t\t{res.total_quantity_sold}\t\t{res.pnl}"
            )


if __name__ == "__main__":
    app()
