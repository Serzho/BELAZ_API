from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

Base = declarative_base()

def load_session() -> (Session, bool):
    db_exists = Path.exists(Path("../belaz.db"))
    engine = create_engine(
        "sqlite:///../belaz.db"
    )  # создание движка базы данных
    Base.metadata.create_all(bind=engine)  # создание базы данных
    return Session(bind=engine), db_exists
