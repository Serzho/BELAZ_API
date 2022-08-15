import sys

import sqlalchemy


from .init_database import Base


class Model(Base):
    __tablename__ = 'model'
    id = sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column("title", sqlalchemy.String(32))
    load_capacity = sqlalchemy.Column("load_capacity", sqlalchemy.Integer)
    engine_power = sqlalchemy.Column("engine_power", sqlalchemy.Integer)
    transmission = sqlalchemy.Column("transmission", sqlalchemy.String(32))
    torque = sqlalchemy.Column("torque", sqlalchemy.Integer)
    fuel_consumption = sqlalchemy.Column("fuel_consumption", sqlalchemy.Integer)
    tires = sqlalchemy.Column("tires", sqlalchemy.String(32))
    max_speed = sqlalchemy.Column("max_speed", sqlalchemy.Integer)
    turning_radius = sqlalchemy.Column("turning_radius", sqlalchemy.Float)
    weight = sqlalchemy.Column("weight", sqlalchemy.Integer)
    id_series = sqlalchemy.Column("id_series", sqlalchemy.Integer, sqlalchemy.ForeignKey("series.id_series"))
    id_author = sqlalchemy.Column("id_author", sqlalchemy.Integer, sqlalchemy.ForeignKey("author.id_author"))

    def __init__(self, title: str, load_capacity: int, engine_power: int, transmission: str,
                 torque: int, fuel_consumption: int, tires: str, max_speed: int,
                 turning_radius: float, weight: int, id_series: int, id_author: int):
        self.title = title
        self.load_capacity = load_capacity
        self.engine_power = engine_power
        self.transmission = transmission
        self.torque = torque
        self.fuel_consumption = fuel_consumption
        self.tires = tires
        self.max_speed = max_speed
        self.turning_radius = turning_radius
        self.weight = weight
        self.id_series = id_series
        self.id_author = id_author

    def get_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "load_capacity": self.load_capacity,
            "engine_power": self.engine_power,
            "transmission": self.transmission,
            "torque": self.torque,
            "fuel_consumption": self.fuel_consumption,
            "tires": self.tires,
            "max_speed": self.max_speed,
            "turning_radius": self.turning_radius,
            "weight": self.weight,
            "id_series": self.id_series,
            "id_author": self.id_author
        }

    def change_by_dict(self, model_dict: dict) -> None:
        if "title" in model_dict:
            self.title = model_dict.get("title")
        if "load_capacity" in model_dict:
            self.load_capacity = model_dict.get("load_capacity")
        if "engine_power" in model_dict:
            self.engine_power = model_dict.get("engine_power")
        if "transmission" in model_dict:
            self.transmission = model_dict.get("transmission")
        if "torque" in model_dict:
            self.torque = model_dict.get("torque")
        if "fuel_consumption" in model_dict:
            self.fuel_consumption = model_dict.get("fuel_consumption")
        if "max_speed" in model_dict:
            self.max_speed = model_dict.get("max_speed")
        if "turning_radius" in model_dict:
            self.turning_radius = model_dict.get("turning_radius")
        if "weight" in model_dict:
            self.weight = model_dict.get("weight")
