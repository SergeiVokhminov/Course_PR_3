from datetime import datetime, date

from config import config
from src.api_work import HeadHunterApi
from src.db_class import DBManager
from src.db_create import create_db
from src.db_save_info import save_info_employer_database
from src.employers_class import Employer
from src.file_work import JobFile
from src.utils import prints_a_greeting, get_employers_id
from src.vacancies_class import Vacancy


def main():
    """
    Функция соединяет работу всех реализованных функций.
    :return: Результат работы реализованных функций.
    """

    # приветствие с пользователем
    prints_a_greeting()

    # Создание экземпляра класса для работы с API
    hh_api = HeadHunterApi()
    # print(hh_api)

    # получение информации о работодателях
    employer = hh_api.get_info_employers()
    # print(employer)
    emp = hh_api.get_load_emp(employer)
    # print(emp)

    print(
        f"Мне удалось найти информацию о более {len(employer)} работодателях.\n"
        f"Из-за большого количества работодателей и вакансий,\n"
        f"оставляю только 10 компаний у которых больше всего объявлений о вакансиях.\n"
    )

    # оставляем 10 работодателей по большему количеству открытых вакансий
    top_employers = emp[:10]
    # print(top_employers)
    # print(len(top_employers))

    # получаем список id работодателей
    id_employers_list = get_employers_id(top_employers)
    print(id_employers_list)
    # print(type(id_employers_list))

    # save_file = JobFile()
    # save_file.save_vacancy_file(top_employers)

    # read_file = save_file.read_file()
    # print(read_file)

    # получаем список вакансий по id работодателя
    vacancies_employer = hh_api.get_vacancies_employer(id_employers_list)
    print(len(vacancies_employer))

    # получение сокращенной информации о вакансиях работодателей
    user_vac_emp = hh_api.get_load_vac_emp(vacancies_employer)

    save_emp_file = JobFile("employers.json")
    save_vac_emp_file = JobFile("vacancies.json")
    # save_file.save_vacancy_file(user_vac_emp)

    # read_file = save_file.read_file()

    print(len(user_vac_emp))

    print("Созданию базу данных db_test")
    params = config()
    create_db("db_test", params)
    #
    print("База данных db_test создана.")
    print("Сохраняем информацию о работодателях в базу данных.")
    save_info_employer_database(
        top_employers,
        user_vac_emp,
        "db_test",
        params,
    )

    print(
        """Что сделать с полученными данными?
    1. Вывести название компании и количество вакансий.
    2. Вывести информацию о вакансиях.
    3. Вывести среднюю зарплату по вакансиям.
    4. Вывести все вакансии у которых зарплата выше средней.
    5. Вывести вакансии по ключевому слову.
    6. Записать данные в файл.
    0. Выйти и сохранить полученные данные в файл."""
    )

    while True:
        user_answers = input("Введите цифру: \n")
        if user_answers in ("1", "2", "3", "4", "5", "6", "0"):
            break
        else:
            print("Введён некорректный ответ. Повторите ввод.")

    menu = {
        "1": "Вывести название компании и количество вакансий.",
        "2": "Вывести информацию о вакансиях.",
        "3": "Вывести среднюю зарплату по вакансиям.",
        "4": "Вывести все вакансии у которых зарплата выше средней.",
        "5": "Вывести вакансии по ключевому слову.",
        "6": "Записать данные в файл.",
        "0": "Выйти и удалить данные из файл.",
    }

    print(f"Для обработки выбрано: {menu.get(user_answers)}\n")

    user_db = DBManager("db_test", params)

    # выводим компании и количество вакансий
    if user_answers == "1":
        all_emp = user_db.get_companies_and_vacancies_count()
        # print(all_emp)
        for key, value in all_emp:
            print(f'"Название компании": {key} | "Количество вакансий": {value} шт.')

    elif user_answers == "2":
        all_vac = user_db.get_all_vacancies()
        for i in all_vac:
            print(
                f"Название компании - {i[0]}\nНазвание вакансии - {i[1]}\n"
                f"Ссылка на вакансию - {i[2]}\nЗарплата - {i[3]}\n"
            )

    elif user_answers == "3":
        salary_vac = user_db.get_avg_salary()
        print(salary_vac)

    elif user_answers == "4":
        salary_vac = user_db.get_vacancies_with_higher_salary()
        print(Vacancy.cast_to_object_list(salary_vac))

    elif user_answers == "5":
        user_input = input("Введите слово для поиска:\n")
        salary_vac = user_db.get_vacancies_with_keyword(user_input)
        print(salary_vac)
        print(len(salary_vac))

    elif user_answers == "6":
        save_emp_file.save_vacancy_file(top_employers)
        save_vac_emp_file.save_vacancy_file(user_vac_emp)
        print("Данные записаны.\nРабота программы завершена.")

    elif user_answers == "0":
        save_emp_file.delete_file()
        save_vac_emp_file.delete_file()
        print("Работа программы завершена.")


if __name__ == "__main__":
    main()

# count_employers = 0
#     for item in Employer.cast_to_object_list(top_employers):
#         print(item)
#         count_employers += 1
#     print(count_employers)
