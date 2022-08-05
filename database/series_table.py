import sqlalchemy

from service import Base


class Series(Base):
    __tablename__ = 'series'
    id_series = sqlalchemy.Column("id_series", sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name_series = sqlalchemy.Column("name_series", sqlalchemy.String(32))

    def __init__(self, name_series: str):
        self.name_series = name_series


