import requests

from src.abstract_class import Parser


class HeadHunterApi(Parser):
    """Класс для работы с API."""

    def __init__(self) -> None:
        """Инициализатор класса HeadHunterApi."""
        self.__url_info_employers = "https://api.hh.ru/employers/"  # получения полной информации о работодателях
        self.__url_vacancies_employers = "https://api.hh.ru/vacancies"  # получение вакансий работодателей
        self.__headers = {"User-Agent": "HH-User-Agent"}
        self.__params_emp = {"page": 0, "per_page": 100, "sort_by": "by_vacancies_open"}
        self.__params_vac_emp = {"page": 0, "per_page": 100, "area": 113, 'only_with_salary': True}
        self.__employers: list[dict] = []
        self.__vacancies_list: list[dict] = []

    def __api_connect(self) -> requests.Response:
        """Метод проверки подключения к API hh.ru"""
        response = requests.get(self.__url_info_employers, headers=self.__headers, params=self.__params_emp)
        if response.status_code == 200:
            # print(response)
            return response
        else:
            print("Ошибка при получении данных", response.status_code)

    def get_info_employers(self) -> list[dict]:
        """Метод получения информации о работодателях."""
        while self.__params_emp.get("page") != 20:
            response = self.__api_connect()
            if response:
                employers = response.json()["items"]
                self.__employers.extend(employers)
                self.__params_emp["page"] += 1
            else:
                break
        return self.__employers

    def get_load_emp(self, __employers: list[dict]):
        """Метод получения информации о работодателях по ключам."""
        emp_list = []

        if self.__employers:
            # получение списка словарей с ключами id, name, url, vac_url, open_vacancies
            for emp in self.__employers:
                emp_id = emp.get("id")
                name = emp.get("name")
                url = emp.get("alternate_url")
                open_vacancies = emp.get("open_vacancies")

                emp_list.append(
                    {
                        "id": emp_id,
                        "name": name,
                        "url": url,
                        "open_vacancies": open_vacancies
                    }
                )

            return emp_list

    def get_vacancies_employer(self, employer_id) -> list[dict]:
        """Метод получения вакансий по id работодателя."""
        self.__params_vac_emp['employer_id'] = employer_id
        while self.__params_vac_emp.get("page") != 20:
            response = requests.get(self.__url_vacancies_employers, headers=self.__headers, params=self.__params_vac_emp)
            if response:
                vacancies_employers = response.json()["items"]
                self.__vacancies_list.extend(vacancies_employers)
                self.__params_vac_emp["page"] += 1
            else:
                break
        return self.__vacancies_list

    def get_load_vac_emp(self, __vacancies_list):
        """Метод получения списка словарей по ключам."""
        vac_emp_list = []

        if self.__vacancies_list:
            # получение списка словарей с ключами id, name, open_vacancies
            for vacancy in self.__vacancies_list:
                id_vac = vacancy.get("id")
                id_emp = vacancy.get('employer').get('id')
                name_vac = vacancy.get("name")
                name_emp = vacancy.get("employer").get("name")
                url = vacancy.get("alternate_url")
                requirement = vacancy.get("snippet").get("requirement")
                responsibility = vacancy.get("snippet").get("responsibility")
                area = vacancy.get("area").get("name")
                if vacancy.get("salary"):
                    if vacancy["salary"]["to"]:
                        salary = vacancy["salary"]["to"]
                    elif vacancy["salary"]["from"]:
                        salary = vacancy["salary"]["from"]
                else:
                    salary = 0

                vac_emp_list.append(
                    {
                        'vacancy_id': id_vac,
                        'employer_id': id_emp,
                        'name_vacancy': name_vac,
                        'name_employer': name_emp,
                        'url': url,
                        'requirement': requirement,
                        'responsibility': responsibility,
                        'area': area,
                        'salary': salary,
                    }
                )

        return vac_emp_list


if __name__ == "__main__":
    user_list_company = [
        {'id': '966757', 'name': 'Группа КОМФОРТ'},
        {'id': '4344489', 'name': 'Точка Пересечения'}
    ]

    hh_api = HeadHunterApi()
    #  получаем всю информацию о работодателях
    emp_info = hh_api.get_info_employers()
    # print(emp_info)
    # print(len(emp_info))

    #  получаем сокращенную информацию о работодателях
    list_emp = hh_api.get_load_emp(emp_info)[:10]
    # print(list_emp)
    # print(len(list_emp))

    # получаем список вакансий работодателя
    vacancies = hh_api.get_vacancies_employer(["3148"])
    # print(vacancies)
    # print(len(vacancies))

    # получаем сокращенную информации о вакансиях работодателя
    list_vacancies = hh_api.get_load_vac_emp(vacancies)
    # print(list_vacancies)
    # print(len(list_vacancies))
