import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import InsecureRequestWarning
import warnings
from database_controller import DatabaseController
from service.service import base_logger


def log(message: str) -> None:
    base_logger(msg=message, module_name="PARSER")


class LineupParser:
    __column_list = [
        "Грузоподъемность, т", "Мощность двигателя, кВт (л.с.)", "Трансмиссия", "Крутящий момент, Н*м (об/мин)",
        "Удельный расход топлива при номинальной мощности, г/ кВт*ч", "Шины", "Максимальная скорость, км/ч",
        "Радиус поворота, м", "Полная масса, кг"
    ]
    __db_controller = None

    def __init__(self, db_controller: DatabaseController) -> None:
        self.__db_controller = db_controller
        warnings.simplefilter('ignore', InsecureRequestWarning)
        log("Belaz parser was initialized!")

    def __get_page_soup(self, url: str) -> BeautifulSoup:
        log(f"Getting page with url = {url}")
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                          'Chrome/72.0.3626.121 Safari/537.36',
            'upgrade-insecure-requests': '1',
            'cookie': 'mos_id=CllGxlx+PS20pAxcIuDnAgA=; '
                      'session-cookie=158b36ec3ea4f5484054ad1fd214'
                      '07333c874ef0fa4f0c8e34387efd5464a1e9500e2277b0'
                      '367d71a273e5b46fa0869a; NSC_WBS-QUBG-jo-nptsv-WT-443'
                      '=ffffffff0951e23245525d5f4f58455e445a4a423660; '
                      'rheftjdd=rheftjddVal; _ym_uid=1552395093355938562; _ym_d=1552395093; _ym_isad=2'
        }
        response = None

        response = requests.get(url=url, headers=headers, verify=False)
        log(f"Page returned with status code = {response.status_code}")
        # print(url)
        # print(len(response.text))
        return BeautifulSoup(response.text, "lxml")

    def __get_links(self, tags: list) -> list:
        log(f"Getting {len(tags)} tags from main page")
        returning_links = []
        for el in tags:
            returning_links.append(f"https://belaz.by{el['href']}")
        return returning_links

    def __parse_main_page(self) -> list:
        log("Parsing main page...")
        main_page_soup = self.__get_page_soup("https://belaz.by/products/products-belaz/dumpers/")
        hydromechanical_table, electromechanical_table = main_page_soup.find_all("table", class_="catalog-table-list")
        log(f"{len(hydromechanical_table)} links found in hydromechanical lineup")
        log(f"{len(electromechanical_table)} links found in electromechanical lineup")
        hydromechanical_lineup = self.__get_links(
            hydromechanical_table.find_all("a", class_="catalog-card-item")
        )
        electromechanical_lineup = self.__get_links(
            electromechanical_table.find_all("a", class_="catalog-card-item")
        )
        # print(len(electromechanical_lineup), len(hydromechanical_lineup))
        lineup = electromechanical_lineup + hydromechanical_lineup
        log("Main page was parsed")
        return lineup

    def __get_models_features(self, model_soup: BeautifulSoup) -> dict:
        # print(model_soup.prettify())
        log(f"Getting features of models")
        models = []
        wrappers = model_soup.find_all("div", class_="accordion__hidden-wrapper")
        model_chars = {}
        names = []
        tabs_wrapper = model_soup.find("div", class_="tabs-wrapper")
        series_title = model_soup.h1.string.split()[-1]
        if tabs_wrapper is not None:
            for name in tabs_wrapper.find_all("div", class_="tabs__item"):
                names.append(name.string)
        else:
            names.append(series_title)
        # print(f"Count of wrappers {len(wrappers)}")
        for wrapper in wrappers:
            rows = wrapper.find_all("div", class_="grid__row")
            # print(f"Count of rows {len(rows)}")
            for row in rows:
                # print(row.prettify())
                field = row.find("p", class_="grid__gray").string
                # print(field)
                if field in self.__column_list and field not in model_chars.keys():
                    all_values = row.find("div", class_="grid__cell width-75").find_all("p")
                    value = ""
                    for el in all_values:
                        try:
                            if el["class"] == ['grid__rus']:
                                value = el.string
                                break
                        except KeyError:
                            if not (el.string is None):
                                value = el.string
                                break

                    model_chars.update({
                        field: value.rstrip()
                    }
                    )
                    # print(f"Count of chars {len(model_chars)}")
                    if len(model_chars) == 9:
                        model_chars.update(
                            {"Название": f"Белаз-{names.pop(0)}"}
                        )
                        models.append(model_chars.copy())
                        model_chars.clear()
        # print(models)
        # print(f"Models of count {len(models)}")
        log(f"Found {len(models)} models in series name {series_title}")
        return {series_title: models}

    def __print_models(self, series: dict) -> None:
        for series_title, models in series.items():
            print(f"MODELS {series_title} SERIES")
            for el in models:
                for key, value in el.items():
                    print(f"{key}: {value}")
                print()
            print()

    def parse(self, remake: bool):
        log(f"Parsing belaz.by: remake = {remake}")
        if remake:
            self.__db_controller.erase_lineup()

        lineup = self.__parse_main_page()
        series = {}

        for link in lineup:
            # print(link)
            page_soup = self.__get_page_soup(link)
            series.update(self.__get_models_features(page_soup))
            # print(len(series))

        # self.__print_models(series)
        self.__db_controller.add_lineup(series)
        log("Belaz.by was parsed!")
