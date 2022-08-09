from pydantic import BaseModel


class Item_reqeust(BaseModel):
    id: int
    title: str


class Add_request(BaseModel):
    title: str
    load_capacity: int
    engine_power: int
    transmission: str
    torque: int
    fuel_consumption: int
    tires: str
    max_speed: int
    turning_radius: float
    weight: int
    name_series: str


class Parse_request(BaseModel):
    remake: bool

class Delete_series_request(BaseModel):
    name_series: bool
