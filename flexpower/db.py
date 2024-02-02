from sqlmodel import Session, SQLModel, create_engine

from flexpower.config import get_settings

config = get_settings()

DATABASE_URL = f"postgresql+psycopg2://{config.postgres_user}:{config.postgres_password}@db:5432/{config.postgres_db}"

engine = create_engine(DATABASE_URL)


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
