from sqlmodel import Session, SQLModel, create_engine

from flexpower.config import get_settings

config = get_settings()
engine = create_engine(config.database_url, connect_args={"check_same_thread": False})


def get_session():
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)
