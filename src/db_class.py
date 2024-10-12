from typing import Any

import psycopg2


class DBManager:
    """Класс для получения информации о работодателях и их вакансиях из базы данных."""

    def __init__(self, db_name: str, params: dict[str, Any]):
        """Инициализатор класса DBManager"""
        self.db_name = db_name
        self.__params = params

    def __connect_database(self) -> Any:
        """Подключение к базе данных"""
        return psycopg2.connect(dbname=self.db_name, **self.__params)

    def get_companies_and_vacancies_count(self) -> list[dict[str, str, Any]]:
        """Метод получает список всех компаний и количество вакансий у каждой компании."""
        conn = self.__connect_database()
        with conn.cursor() as cur:
            cur.execute("""SELECT employer_name, open_vacancies FROM employers""")
            emp_vacs = cur.fetchall()

        conn.close()

        return emp_vacs

    def get_all_vacancies(self):
        """Метод получает список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию."""
        conn = self.__connect_database()
        with conn.cursor() as cur:
            cur.execute("""SELECT employer_name, vacancy_name, url, salary FROM vacancies""")
            vacs = cur.fetchall()

        conn.close()

        return vacs

    def get_avg_salary(self):
        """Метод получает среднюю зарплату по вакансиям."""
        conn = self.__connect_database()
        with conn.cursor() as cur:
            cur.execute("SELECT AVG(salary) FROM vacancies")
            salary = round(cur.fetchone()[0])

        conn.close()

        return salary

    def get_vacancies_with_higher_salary(self):
        """Метод получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        conn = self.__connect_database()
        with conn.cursor() as cur:
            cur.execute("""SELECT * FROM vacancies where salary > (select avg(salary) desc from vacancies)""")
            higher_salary = cur.fetchall()

        conn.close()

        return higher_salary

    def get_vacancies_with_keyword(self, keyword: str):
        """Метод получает список всех вакансий,
        в которых содержится переданное в метод слово, например python."""
        conn = self.__connect_database()
        with conn.cursor() as cur:
            cur.execute(f"""SELECT * FROM vacancies WHERE vacancy_name LIKE '%{keyword}%' 
                            OR employer_name LIKE '%{keyword}%' 
                            OR requirement LIKE '%{keyword}%' 
                            OR responsibility LIKE '%{keyword}%' 
                            OR area LIKE '%{keyword}%' """
                        )
            all_vac = cur.fetchall()

        conn.close()

        return all_vac


if __name__ == "__main__":
    pass
