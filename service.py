import logging
from datetime import datetime
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


def load_session() -> (Session, bool):
    db_exists = Path.exists(Path("belaz.db"))
    engine = create_engine(
        "sqlite:///belaz.db"
    )  # создание движка базы данных
    Base.metadata.create_all(bind=engine)  # создание базы данных
    return Session(bind=engine), db_exists


def base_logger(msg: str, module_name: str) -> None:
    time = datetime.now().time()
    logging.info(f" {time.strftime('%H:%M:%S')} {module_name}: {msg}")