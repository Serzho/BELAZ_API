import sys

sys.path.append("../")

from parser import LineupParser
from core.database_controller import DatabaseController
from fastapi import FastAPI
from service.logger import create_logger, base_logger

create_logger("../log.txt")
base_logger("Application started!", module_name="SERVER")

dbController = DatabaseController()
parser = LineupParser(dbController)

fastAPI_app = FastAPI()  # создание приложения fast_api
