from core.parser import LineupParser
from database.database_controller import DatabaseController
from fastapi import FastAPI


dbController = DatabaseController()
parser = LineupParser(dbController)

app = FastAPI()  # создание приложения fast_api
