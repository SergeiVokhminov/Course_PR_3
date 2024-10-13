import pytest

from typing import Any


@pytest.fixture
def employers_dict() -> Any:
    vacs = [
        {
            "employer_id": "123321",
            "employer_name": "Gazprom",
            "employer_url": "https://test_1",
            "open_vacancies": 340,
        },
        {
            "employer_id": "123321",
            "employer_name": "Программист_2",
            "employer_url": "https://test_2",
            "open_vacancies": 200,
        },
    ]

    return vacs


@pytest.fixture
def vacancies_dict() -> Any:
    vacs = [
        {
            "vacancy_id": "1",
            "employer_id": "1",
            "vacancy_name": "Программист_1",
            "employer_name": "Vb",
            "url": "https://test_1",
            "requirement": "Требования_1",
            "responsibility": "Обязанности_1",
            "area": "Город_1",
            "salary": 10000,
        },
        {
            "vacancy_id": "2",
            "employer_id": "2",
            "vacancy_name": "Программист_2",
            "employer_name": "Tb",
            "url": "https://test_2",
            "requirement": "Требования_2",
            "description": "Обязанности_2",
            "area": "Город_2",
            "salary": 15000,
        },
    ]

    return vacs


@pytest.fixture
def file_name() -> Any:
    return "test_file_vacancy.json"
