from typing import Any

import psycopg2


def save_info_employer_database(
    employers: list[dict[str, Any]], vacancies: list[dict[str, Any]], db_name: str, params: dict[str, Any]
) -> None:
    """Функция заполнения таблицы данными о работодателях"""

    conn = psycopg2.connect(dbname=db_name, **params)

    with conn.cursor() as cur:
        for employer in employers:
            employer_id = employer.get("employer_id")
            employer_name = employer.get("employer_name")
            employer_url = employer.get("employer_url")
            open_vacancies = employer.get("open_vacancies")
            # заполняем таблицу employers
            cur.execute(
                """INSERT INTO employers (
                employer_id, employer_name, employer_url, open_vacancies)
                VALUES (%s, %s, %s, %s)""",
                (employer_id, employer_name, employer_url, open_vacancies),
            )

        # заполняем таблицу vacancies
        for vacancy in vacancies:
            vacancy_id = vacancy.get("vacancy_id")
            employer_id = vacancy.get("employer_id")
            vacancy_name = vacancy.get("vacancy_name")
            employer_name = vacancy.get("employer_name")
            url = vacancy.get("url")
            requirement = vacancy.get("requirement")
            responsibility = vacancy.get("responsibility")
            area = vacancy.get("area")
            salary = vacancy.get("salary")
            cur.execute(
                """
                INSERT INTO vacancies (vacancy_id, employer_id, vacancy_name, employer_name, url, 
                                        requirement, responsibility, area, salary)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                (vacancy_id, employer_id, vacancy_name, employer_name, url, requirement, responsibility, area, salary),
            )

    conn.commit()
    conn.close()
