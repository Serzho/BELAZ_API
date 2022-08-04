import sqlalchemy

from service import Base


class Author(Base):
    __tablename__ = 'author'
    id = sqlalchemy.Column("id_author", sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name_series = sqlalchemy.Column("name_author", sqlalchemy.String(32))

    def __init__(self, name_author: str):
        self.name_author = name_author


