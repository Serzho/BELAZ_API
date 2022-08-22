import sys

sys.path.append("../")
sys.path.append("../core")
from core.parser import LineupParser
from core.database_controller import DatabaseController
from fastapi import FastAPI
from .service.logger import create_logger, base_logger
from cfg import LOG_NAME

create_logger(f"../{LOG_NAME}")
base_logger("Application started!", module_name="SERVER")

dbController = DatabaseController()
belaz_parser = LineupParser(dbController)

fastAPI_app = FastAPI()  # создание приложения fast_api
