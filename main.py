from config import config
from src.api_work import HeadHunterApi
from src.db_class import DBManager
from src.db_create import create_db
from src.db_save_info import save_info_employer_database

from src.file_work import JobFile
from src.utils import get_employers_id, prints_a_greeting, get_name_employers


def main() -> None:
    """
    Функция соединяет работу всех реализованных функций.
    :return: Результат работы реализованных функций.
    """

    # приветствие с пользователем
    prints_a_greeting()

    # Создание экземпляра класса для работы с API
    print("Загружаю информацию по работодателям и их вакансиям. Подождите ...\n")
    hh_api = HeadHunterApi()

    # получение полную информации о работодателях
    employer = hh_api.get_info_employers()

    # получаем сокращенную информацию о работодателях
    emp = hh_api.get_load_emp(employer)

    print(
        f"Мне удалось найти информацию о более {len(employer)} работодателях.\n"
        f"Из-за большого количества работодателей и вакансий,\n"
        f"оставляю только 10 компаний у которых больше всего объявлений о вакансиях.\n"
    )

    # оставляем 10 работодателей по большему количеству открытых вакансий
    top_employers = emp[:10]

    # получаем список id работодателей
    id_employers_list = get_employers_id(top_employers)

    # получаем список имен работодателей
    name_emp_list = get_name_employers(top_employers)

    # получаем список вакансий по id работодателя
    vacancies_employer = hh_api.get_vacancies_employer(id_employers_list)

    # получение сокращенной информации о вакансиях работодателей
    user_vac_emp = hh_api.get_load_vac_emp(vacancies_employer)

    print("Создаю базу данных db_test для хранения информации")
    params = config()
    create_db("db_test", params)

    print("База данных db_test успешно создана.")
    print("Сохраняю информацию о работодателях и их вакансиях в базу данных.\n")
    save_info_employer_database(
        top_employers,
        user_vac_emp,
        "db_test",
        params,
    )

    print(f"Для обработки выбраны следующие компании:\n{name_emp_list}")

    print(
        """Что сделать с полученными данными?
    1. Вывести название компании и количество вакансий.
    2. Вывести информацию о вакансиях.
    3. Вывести среднюю зарплату по вакансиям.
    4. Вывести все вакансии у которых зарплата выше средней.
    5. Вывести вакансии по ключевому слову.
    6. Записать информацию в файл.
    0. Выйти и удалить полученные данные в файл.\n"""
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

    # выводим из базы данных компании и количество вакансий
    if user_answers == "1":
        count = 0
        all_emp = user_db.get_companies_and_vacancies_count()
        for key, value in all_emp:
            print(f'"Название компании": {key} | "Количество вакансий": {value} шт.')
            count += int(value)

        print(f"\nКоличество компаний - {len(all_emp)} шт.\nОбщее количество вакансий - {count} шт.")

    # выводим из базы данных информацию о вакансиях
    elif user_answers == "2":
        all_vac = user_db.get_all_vacancies()
        count = 0
        for i in all_vac:
            count += 1
            print(
                f"Название компании - {i[0]}\nНазвание вакансии - {i[1]}\n"
                f"Ссылка на вакансию - {i[2]}\nЗарплата - {i[3]}\n"
            )
        print(f"Количество вакансий - {count} шт.")

    # выводим из базы данных информацию о средней зарплате по всем вакансиям
    elif user_answers == "3":
        salary_vac = user_db.get_avg_salary()
        print(f"Средняя зарплата по всем вакансиям - {salary_vac} руб.")

    # выводим из базы данных информацию о вакансиях у которых зарплаты больше средней
    elif user_answers == "4":
        salary_vac = user_db.get_vacancies_with_higher_salary()
        count = 0
        for item in salary_vac:
            count += 1
            print(
                f"ID вакансии - {item[0]},\nID компании - {item[1]},\nНазвание вакансии - {item[2]},\n"
                f"Название компании - {item[3]}\nСсылка на вакансию - {item[4]}\nТребования - {item[5]},\n"
                f"Описание - {item[6]},\nГород - {item[7]},\nЗарплата - {item[8]}\n"
            )

        print(f"Количество вакансий - {count} шт.")

    # выводим из базы данных информацию о вакансиях по ключевому слову
    elif user_answers == "5":
        user_input = input("Введите слово для поиска:\n")
        salary_vac = user_db.get_vacancies_with_keyword(user_input)
        count = 0
        for item in salary_vac:
            if len(salary_vac) > 0:
                print(
                    f"ID вакансии - {item[0]},\nID компании - {item[1]},\nНазвание вакансии - {item[2]},\n"
                    f"Название компании - {item[3]}\nСсылка на вакансию - {item[4]}\nТребования - {item[5]},\n"
                    f"Описание - {item[6]},\nГород - {item[7]},\nЗарплата - {item[8]}\n"
                )
                count += 1
            else:
                print("Данные отсутствуют!")
        print(f"Количество найденных вакансий по ключевому слову - {count} шт.")

    # сохраняем полученную информацию с hh.ru в файлы
    elif user_answers == "6":
        save_emp_file = JobFile("employers.json")
        save_vac_emp_file = JobFile("vacancies.json")
        save_emp_file.save_vacancy_file(top_employers)
        save_vac_emp_file.save_vacancy_file(user_vac_emp)
        print("Данные сохранены.\nРабота программы завершена.")

    # выходим из программы и удаляем сохраненную информацию в файлах
    elif user_answers == "0":
        save_emp_file = JobFile("employers.json")
        save_vac_emp_file = JobFile("vacancies.json")
        save_emp_file.delete_file()
        save_vac_emp_file.delete_file()
        print("Данные удалены.\nРабота программы завершена.")


if __name__ == "__main__":
    main()
