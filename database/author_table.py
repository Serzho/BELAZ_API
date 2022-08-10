import sqlalchemy

from core.service import Base


class Author(Base):
    __tablename__ = 'author'
    id_author = sqlalchemy.Column("id_author", sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name_author = sqlalchemy.Column("name_author", sqlalchemy.String(32))

    def __init__(self, name_author: str):
        self.name_author = name_author


