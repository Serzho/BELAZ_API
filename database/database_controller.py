from service import load_session
from database.model_table import Model
from database.series_table import Series
from database.author_table import Author


class DatabaseController:
    __session = None

    def __init__(self) -> None:
        self.__session, db_exists = load_session()
        if not db_exists:
            self.add_author("PARSER")

    def add_author(self, name_author: str) -> None:
        author = Author(name_author)
        try:
            self.__session.add(author)
            self.__session.commit()
        except Exception as e:
            print(e)


    def add_series(self, name_series: str) -> None:
        query = self.__session.query(Series.name_series).filter(Series.name_series == name_series).count()
        if query:
            print(f"Series with name {name_series} already exists!")
        else:
            try:
                adding_series = Series(name_series)
                self.__session.add(adding_series)
                self.__session.commit()
                print(f"Series with name {name_series} was added!")
            except Exception as e:
                print(e)

    def add_model(self, model_dict: dict, name_series: str, name_author: str) -> None:
        id_author = self.__session.query(Author).filter(
            Author.name_author == name_author
        ).first().id_author

        id_series = self.__session.query(Series).filter(
            Series.name_series == name_series
        ).first().id_series

        model = Model(
            title=model_dict.get("title"),
            load_capacity = model_dict.get("load_capacity"),
            engine_power = model_dict.get("engine_power"),
            transmission = model_dict.get("transmission"),
            torque = model_dict.get("torque"),
            fuel_consumption = model_dict.get("fuel_consumption"),
            tires = model_dict.get("tires"),
            max_speed = model_dict.get("max_speed"),
            turning_radius = model_dict.get("turning_radius"),
            weight = model_dict.get("weight"),
            id_series = id_series,
            id_author = id_author
        )

        try:
            self.__session.add(model)
            self.__session.commit()
        except Exception as e:
            print(e)

    def __handle_model_dict(self, input_dict: dict) -> dict:
        output_dict = {}
        try:
            output_dict.update(
                {
                    "title": input_dict.get("Название"),
                    "load_capacity": int(input_dict.get("Грузоподъемность, т").split("-")[-1]),
                    "engine_power": int(input_dict.get("Мощность двигателя, кВт (л.с.)").split(";")[-1].split("(")[1][:-1]),
                    "transmission": input_dict.get("Трансмиссия"),
                    "torque": int(input_dict.get("Крутящий момент, Н*м (об/мин)").split()[-1].replace("(", "").replace(")", "").replace("/", "").replace("-", "")[-1]),
                    "fuel_consumption": input_dict.get("Удельный расход топлива при номинальной мощности, г/ кВт*ч"),
                    "tires": input_dict.get("Шины"),
                    "max_speed": int(input_dict.get("Максимальная скорость, км/ч")),
                    "turning_radius": float(input_dict.get("Радиус поворота, м").replace(",", ".")),
                    "weight": int(input_dict.get("Полная масса, кг").replace(" ", "").split("-")[-1].split("—")[-1].replace(u"\xa0", u""))
                }
            )
        except ValueError as ve:
            print(input_dict.get("Название"))
            print(ve)

        return output_dict

    def add_lineup(self, lineup_dict: dict) -> None:
        for name_series, models in lineup_dict.items():
            self.add_series(name_series)
            for model in models:
                model_dict = self.__handle_model_dict(model)
                self.add_model(model_dict, name_series, "PARSER")


