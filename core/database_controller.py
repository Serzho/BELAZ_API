from database.init_database import load_session
from database.model_table import Model
from database.series_table import Series
from database.author_table import Author
from sqlalchemy.exc import OperationalError
from service.logger import base_logger


def log(message: str) -> None:
    base_logger(msg=message, module_name="DATABASE")


class DatabaseController:
    __session = None

    def __init__(self) -> None:
        self.__session, db_exists = load_session()
        if not db_exists:
            self.add_author("PARSER")
            self.add_author("USER")
        log("Database controller was initialized!")

    def add_author(self, name_author: str) -> None:
        log(f"Adding author with name = {name_author}")
        author = Author(name_author)
        try:
            self.__session.add(author)
            self.__session.commit()
        except Exception as e:
            log("Traceback error!")
            print(e)

    def add_series(self, name_series: str) -> None:
        log(f"Adding series with name = {name_series}")
        query = self.__session.query(Series.name_series).filter(Series.name_series == name_series).count()
        if query:
            log(f"Series with name {name_series} already exists!")
        else:
            try:
                adding_series = Series(name_series)
                self.__session.add(adding_series)
                self.__session.commit()
                log(f"Series with name {name_series} was added!")
            except Exception as e:
                log("Traceback error!")
                print(e)

    def add_model(self, model_dict: dict, name_series: str, name_author: str) -> str:
        log(f"Adding model {model_dict.get('title')} from series {name_series} by author {name_author}")
        if not self.__session.query(Model.title).filter(Model.title == model_dict.get("title")).count():
            id_author = self.__session.query(Author).filter(
                Author.name_author == name_author
            ).first().id_author

            self.add_series(name_series)

            id_series = self.__session.query(Series).filter(
                Series.name_series == name_series
            ).first().id_series

            model = Model(
                title=model_dict.get("title"),
                load_capacity=model_dict.get("load_capacity"),
                engine_power=model_dict.get("engine_power"),
                transmission=model_dict.get("transmission"),
                torque=model_dict.get("torque"),
                fuel_consumption=model_dict.get("fuel_consumption"),
                tires=model_dict.get("tires"),
                max_speed=model_dict.get("max_speed"),
                turning_radius=model_dict.get("turning_radius"),
                weight=model_dict.get("weight"),
                id_series=id_series,
                id_author=id_author
            )
            log('MODEL DICT: \n'
                ''
                'title = title=model_dict.get("title") \n'
                'load_capacity=model_dict.get("load_capacity") \n'
                'engine_power=model_dict.get("engine_power")\n'
                'transmission=model_dict.get("transmission")\n'
                'torque=model_dict.get("torque")\n'
                'fuel_consumption=model_dict.get("fuel_consumption")\n'
                'tires=model_dict.get("tires")\n'
                'max_speed=model_dict.get("max_speed")\n'
                'turning_radius=model_dict.get("turning_radius")\n'
                'weight=model_dict.get("weight")\n'
                'id_series=id_series\n'
                'id_author=id_author')
            try:
                self.__session.add(model)
                self.__session.commit()
                log(f"Model {model_dict.get('title')} was successfully added!")
                return "Successfully adding"
            except Exception as e:
                print(e)
                log("Traceback error!")
                return "Unsuccessfully deleting"
        else:
            log("Model already exists")
            return "Model already exists"

    def __handle_string(self, string: str) -> str:
        # print(string)
        out_string = string.replace(u"\xa0", u"")
        out_string = out_string.replace(",", ".")
        out_string = out_string.replace(" ", "")
        chars = ["(", ")", "/", "-", "—", ";"]
        for ch in chars:
            if out_string.count(ch) > 0:
                out_string = out_string.replace(ch, " ")

        out_string = out_string.split()[-1]
        log(f"Handle string: before = {string}, after = {out_string}")
        return out_string

    def __handle_model_dict(self, input_dict: dict) -> dict:
        output_dict = {}
        # TODO: Исправить проблему с разными единицами измерения
        try:
            output_dict.update(
                {
                    "title": input_dict.get("Название"),
                    "load_capacity": int(self.__handle_string(input_dict.get("Грузоподъемность, т"))),
                    "engine_power": int(self.__handle_string(input_dict.get("Мощность двигателя, кВт (л.с.)"))),
                    "transmission": input_dict.get("Трансмиссия").split()[0],
                    "torque": int(self.__handle_string(input_dict.get("Крутящий момент, Н*м (об/мин)"))),
                    "fuel_consumption": int(self.__handle_string(
                        input_dict.get("Удельный расход топлива при номинальной мощности, г/ кВт*ч"))),
                    "tires": input_dict.get("Шины"),
                    "max_speed": int(input_dict.get("Максимальная скорость, км/ч")),
                    "turning_radius": float(self.__handle_string(input_dict.get("Радиус поворота, м"))),
                    "weight": int(self.__handle_string(input_dict.get("Полная масса, кг")))
                }
            )
        except ValueError as ve:
            print(input_dict.get("Название"))
            print(ve)

        return output_dict

    def filter_models(self, fields_dict: dict):
        log("Filter models in database: ")
        full_lineup = self.get_all_items()
        log(f"Count of models in full_lineup = {len(fields_dict)}, \nfilter: {fields_dict.items()}")
        filtered_lineup = []
        for model in full_lineup:
            for field_name, condition in fields_dict.items():
                operator = condition[0]
                condition = condition[1:]
                if operator == "=":
                    if not (model.get(field_name) == condition):
                        break
                elif operator == ">":
                    digit = float(condition)
                    if not (model.get(field_name) > digit):
                        break
                elif operator == "<":
                    digit = float(condition)
                    if not (model.get(field_name) < digit):
                        break
            else:
                filtered_lineup.append(model)
        log(f"Filtered {len(filtered_lineup)} items")
        return filtered_lineup

    def edit_model(self, changing_fields, id) -> str:
        log(f"Editing model with id = {id}")
        model = self.get_model(
            id=id
        )
        model.change_by_dict(changing_fields)
        try:
            self.__session.commit()
            log("Successful editing")
            return "Successful editing"
        except Exception as e:
            print(e)
            log("Unsuccessful editing")
            return "Unsuccessful editing"

    def add_lineup(self, lineup_dict: dict) -> None:
        for name_series, models in lineup_dict.items():
            self.add_series(name_series)
            for model in models:
                model_dict = self.__handle_model_dict(model)
                self.add_model(model_dict, name_series, "PARSER")

    def get_all_items(self) -> list[dict]:
        log("Getting all items from database")
        lineup_dict = []
        lineup = self.__session.query(Model).all()
        for model in lineup:
            model_dict = model.get_dict()
            series_name = self.__session.query(
                Series.id_series, Series.name_series
            ).filter(
                Series.id_series == model_dict.pop("id_series")
            ).first().name_series
            author_name = self.__session.query(
                Author.id_author, Author.name_author
            ).filter(
                Author.id_author == model_dict.pop("id_author")
            ).first().name_author
            model_dict.update({
                "series": series_name,
                "author": author_name
            })
            lineup_dict.append(model_dict)
        log(f"Founded {len(lineup_dict)} models in database")
        return lineup_dict

    def get_model(self, id: int, title=None) -> Model:
        model = None
        log(f"Getting model with id = {id} and title = {title} from database")
        if id is not None:
            model = self.__session.query(Model).filter(Model.id == id).first()
        elif title is not None:
            model = self.__session.query(Model).filter(Model.title == title).first()
        return model

    def delete_model(self, id: int, title: str) -> str:
        log(f"Deleting model from database with id = {id} and title = {title}")
        model = self.get_model(id, title)
        if model is not None:
            try:
                self.__session.delete(model)
                self.__session.commit()
                log("Successful deleting")
                return "Successful deleting"
            except Exception as e:
                print(e)
                log("Unsuccessful deleting")
                return "Unsuccessful deleting"
        else:
            log("Model is not found")
            return "Model is not found"

    def erase_lineup(self) -> None:
        log("Erasing lineup...")
        try:
            query = self.__session.query(Series.id_series).all()
            for series in query:
                self.delete_series(id_series=series.id_series, name_series=None)
        except OperationalError:
            pass
        log("Lineup was erased!")

    def delete_series(self, id_series, name_series):
        log(f"Deleting all models with series id = {id_series} and name = {name_series}")
        if name_series is not None:
            id_series = self.__session.query(
                Series.id_series, Series.name_series
            ).filter(Series.name_series == name_series).first().id_series
        # print(id_series)
        query = self.__session.query(Model).filter(Model.id_series == id_series).all()
        log(f"{len(query)} models to delete!")
        for model in query:
            try:
                log(f"Model with id = {model.id} to delete")
                self.__session.delete(model)
                self.__session.commit()
                log("Successful deleting")
            except Exception as e:
                log("Unsuccessful deleting")
                print(e)

        try:
            series = self.__session.query(Series).filter(Series.id_series == id_series).first()
            log(f"Deleting series with name = {series.name_series}")
            self.__session.delete(series)
            self.__session.commit()
            log("Successful deleting")
        except Exception as e:
            log("Unsuccessful deleting")
            print(e)
