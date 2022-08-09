from parser.parser import LineupParser
from database.database_controller import DatabaseController
from fastapi import FastAPI
import uvicorn

dbController = DatabaseController()
parser = LineupParser(dbController)

app = FastAPI()  # создание приложения fast_api
uvicorn.run(app=app, host="localhost", port=9999)