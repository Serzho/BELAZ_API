from sqlalchemy.ext.declarative import declarative_base
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from cfg import DB_USER, DB_PATH
Base = declarative_base()


def load_session() -> (Session, bool):
    db_exists = Path.exists(Path(f"{DB_PATH}"))
    engine = create_engine(
        f"{DB_USER}:///{DB_PATH}"
    )  # создание движка базы данных
    Base.metadata.create_all(bind=engine)  # создание базы данных
    return Session(bind=engine), db_exists
