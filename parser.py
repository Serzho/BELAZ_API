import re

from bs4 import BeautifulSoup
import requests


class LineupParser:
    __column_list = [
        "Применение", "Грузоподъемность, т", "Мощность двигателя, кВт (л.с.)", "Трансмиссия", "Диапазон передач",
        "Крутящий момент, Н*м (об/мин)", "Удельный расход топлива при номинальной мощности, г/ кВт*ч",
        "Шины", "Максимальная скорость, км/ч", "Радиус поворота, м", "Эксплуатационная масса, кг", "Полная масса, кг"
    ]

    def __init__(self) -> None:
        print("Lineup parser was created!")

    def __get_page_soup(self, url: str) -> BeautifulSoup:
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
        response = requests.get(url=url, headers=headers)
        # print(url)
        # print(len(response.text))
        return BeautifulSoup(response.text, "lxml")

    def __get_links(self, tags: list) -> list:
        returning_links = []
        for el in tags:
            returning_links.append(f"https://belaz.by{el['href']}")
        return returning_links

    def __parse_main_page(self) -> tuple[list, list]:
        main_page_soup = self.__get_page_soup("https://belaz.by/products/products-belaz/dumpers/")
        hydromechanical_table, electromechanical_table = main_page_soup.find_all("table", class_="catalog-table-list")
        hydromechanical_lineup = self.__get_links(
            hydromechanical_table.find_all("a", class_="catalog-card-item")
        )
        electromechanical_lineup = self.__get_links(
            electromechanical_table.find_all("a", class_="catalog-card-item")
        )
        return hydromechanical_lineup, electromechanical_lineup

    def __get_models_features(self, model_soup: BeautifulSoup) -> list[dict]:
        models = []
        wrappers = model_soup.find_all("div", class_="accordion__hidden-wrapper")
        model_chars = {}
        for wrapper in wrappers:
            rows = wrapper.find_all("div", class_="grid__row")
            for row in rows:
                # print(row.prettify())
                field = row.find("p", class_="grid__gray").string
                if field in self.__column_list:
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

                    if field == "Применение":
                        field = "Название"
                        pattern = r"БЕЛАЗ-[-+]?\d+."  # Слово "Белаз-", затем любое целое число и буква
                        match = re.search(pattern, value)  # Поиск названия модели
                        value = match[0] if match else 'Not found'

                    model_chars.update({
                        field: value
                    }
                    )
                    if len(model_chars) == 12:
                        models.append(model_chars.copy())
                        model_chars.clear()
        return models

    def temp(self):
        hydromechanical_lineup, electromechanical_lineup = self.__parse_main_page()
        link = hydromechanical_lineup[0]
        page_soup = self.__get_page_soup(link)
        models = self.__get_models_features(page_soup)
        for el in models:
            for key, value in el.items():
                print(f"{key}: {value}")
            print()