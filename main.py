from parser import LineupParser
from database.database_controller import DatabaseController


dbController = DatabaseController()

parser = LineupParser(dbController)
parser.parse()

