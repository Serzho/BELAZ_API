from service import load_session
from database.model_table import Model
from database.series_table import Series
from database.author_table import Author


class DatabaseController:
    session = None

    def __init__(self):
        self.session, __db_exists = load_session()
