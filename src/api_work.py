import requests

from src.abstract_class import Parser
from typing import Any


class HeadHunterApi(Parser):
    """Класс для работы с API."""

    def __init__(self) -> None:
        """Инициализатор класса HeadHunterApi."""
        self.__url_info_employers = "https://api.hh.ru/employers"  # получения полной информации о работодателях
        self.__url_vacancies_employers = "https://api.hh.ru/vacancies"  # получение вакансий работодателей
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params_emp = {"page": 0, "per_page": 100, "sort_by": "by_vacancies_open"}
        self.__params_vac_emp = {"page": 0, "per_page": 100, "area": 113, "only_with_salary": True}
        self.__employers_list: list[dict] = []
        self.__vacancies_employer_list: list[dict] = []

    def __api_connect(self) -> requests.Response:
        """Метод проверки подключения к API hh.ru"""
        response = requests.get(self.__url_info_employers, headers=self.__headers, params=self.__params_emp)
        if response.status_code == 200:
            return response
        else:
            print("Ошибка при получении данных", response.status_code)

    def get_info_employers(self) -> Any:
        """Метод получения информации о работодателях."""
        while self.__params_emp.get("page") != 20:
            response = self.__api_connect()
            if response:
                employers = response.json()["items"]
                self.__employers_list.extend(employers)
                self.__params_emp["page"] += 1
            else:
                break
        return self.__employers_list

    def get_load_emp(self, __employers: list[dict]) -> list[dict]:
        """Метод получения информации о работодателях по определенным ключам."""
        emp_list = []

        if self.__employers_list:
            for emp in self.__employers_list:
                emp_id = emp.get("id")
                name = emp.get("name")
                url = emp.get("alternate_url")
                open_vacancies = emp.get("open_vacancies")
                emp_list.append(
                    {
                        "employer_id": emp_id,
                        "employer_name": name,
                        "employer_url": url,
                        "open_vacancies": open_vacancies,
                    }
                )
        return emp_list

    def get_vacancies_employer(self, employer_id: list):
        """Метод получения вакансий по id работодателя."""
        # self.__params_vac_emp["employer_id"] = employer_id
        # while self.__params_vac_emp.get("page") != 1:
        for item in employer_id:
            url = f"{self.__url_vacancies_employers}?employer_id={item}"
            # print(url)
            response = requests.get(url, headers=self.__headers, params=self.__params_vac_emp)
            if response:
                vacancies_employers = response.json()["items"]
                self.__vacancies_employer_list.extend(vacancies_employers)
                # self.__params_vac_emp["page"] += 1
            else:
                break
        return self.__vacancies_employer_list

    def get_load_vac_emp(self, __vacancies_list: list[dict]):
        """Метод получения списка вакансий работодателй по определенным ключам."""
        vac_emp_list = []

        if self.__vacancies_employer_list:
            for vacancy in self.__vacancies_employer_list:
                id_vac = vacancy.get("id")
                name_vac = vacancy.get("name")
                employer_id = vacancy.get("employer").get("id")
                name_emp = vacancy.get("employer").get("name")
                url = vacancy.get("alternate_url")
                if vacancy.get("snippet").get("requirement"):
                    requirement = vacancy.get("snippet").get("requirement")
                else:
                    requirement = "Данные отсутствуют"
                responsibility = vacancy.get("snippet").get("responsibility")
                if vacancy.get("area").get("name"):
                    area = vacancy.get("area").get("name")
                else:
                    area = "Данные отсутствуют"
                if vacancy.get("salary"):
                    if vacancy["salary"]["to"]:
                        salary = vacancy["salary"]["to"]
                    elif vacancy["salary"]["from"]:
                        salary = vacancy["salary"]["from"]
                else:
                    salary = 0

                vac_emp_list.append(
                    {
                        "vacancy_id": id_vac,
                        "employer_id": employer_id,
                        "vacancy_name": name_vac,
                        "employer_name": name_emp,
                        "url": url,
                        "requirement": requirement,
                        "responsibility": responsibility,
                        "area": area,
                        "salary": salary,
                    }
                )

        return vac_emp_list


if __name__ == "__main__":
    hh_api = HeadHunterApi()
    #  получаем всю информацию о работодателях
    emp_info = hh_api.get_info_employers()
    print(emp_info)

    #  получаем сокращенную информацию о работодателях
    user_list_employers = hh_api.get_load_emp(emp_info)
    print(user_list_employers)

    user_id_list = ("3148", "2060086", "4623486")

    #  получаем вакансии работодателя по его id
    vacancies = hh_api.get_vacancies_employer(user_id_list)  # "2060086", "4623486"
    print(vacancies)

    # получаем сокращенную информации о вакансиях работодателя
    list_vacancies = hh_api.get_load_vac_emp(vacancies)
    print(list_vacancies)
