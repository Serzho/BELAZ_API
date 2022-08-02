from bs4 import BeautifulSoup
import requests


class LineupParser:
    def __init__(self) -> None:
        print("Lineup parser was created!")

    def __get_content(self, url: str) -> str:
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
        return response.text

    def __get_links(self, tags: list) -> list:
        returning_links = []
        for el in tags:
            returning_links.append(f"https://belaz.by/{el['href']}")
        return returning_links

    def get_main_page(self) -> None:
        main_page_soup = BeautifulSoup(self.__get_content("https://belaz.by/products/products-belaz/dumpers/"), "lxml")
        # print(main_page_soup.prettify())
        hydromechanical_table, electromechanical_table = main_page_soup.find_all("table", class_="catalog-table-list")
        hydromechanical_lineup = self.__get_links(
            hydromechanical_table.find_all("a", class_="catalog-card-item")
        )
        electromechanical_lineup = self.__get_links(
            electromechanical_table.find_all("a", class_="catalog-card-item")
        )
        print(hydromechanical_lineup, "\n\n\n\n\n", electromechanical_lineup)