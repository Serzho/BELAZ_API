from parser import LineupParser
from database.database_controller import DatabaseController

parser = LineupParser()
parser.parse()
dbController = DatabaseController()