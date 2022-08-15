import sys

sys.path.append("../")

from parser import LineupParser
from core.database_controller import DatabaseController
from fastapi import FastAPI


dbController = DatabaseController()
parser = LineupParser(dbController)

fastAPI_app = FastAPI()  # создание приложения fast_api
