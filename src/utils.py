from datetime import datetime
from typing import Any


def prints_a_greeting() -> Any:
    """Функция выводит приветствие в зависимости от текущего времени."""

    user_name = input("Введите Ваше имя:\n")
    # logger.info("Функция prints_a_greeting начало работу.")
    greeting_dict = {
        "1": ("Доброе утро, ", "05:00:01", "12:00:00"),
        "2": ("Добрый день, ", "12:00:01", "18:00:00"),
        "3": ("Добрый вечер, ", "18:00:01", "23:59:59"),
        "4": ("Доброй ночи, ", "00:00:00", "05:00:00"),
    }
    try:
        datatime_now = datetime.now()
        str_date_now = datatime_now.strftime("%d-%m-%Y")
        str_time_now = datatime_now.strftime("%H:%M:%S")
        time_greeting = datatime_now.time()
        # logger.info("Функция анализирует и обрабатывает полученные данные.")
        for item in greeting_dict:
            start = greeting_dict[item][1]
            finish = greeting_dict[item][2]
            start_time = datetime.strptime(start, "%H:%M:%S").time()
            finish_time = datetime.strptime(finish, "%H:%M:%S").time()
            if start_time <= time_greeting <= finish_time:
                # logger.info("Функция prints_a_greeting завершила работу и вывела результат.")
                print(f"{greeting_dict.get(item)[0]}{user_name}!\nСегодня: {str_date_now}\nВремя: {str_time_now}")
    except Exception:
        # logger.info("Функция prints_a_greeting завершила работу с ошибкой.")
        raise ValueError("Введены неверные данные!")


def get_employers_id(employers_list: list[dict]) -> list:
    """Функция получения id работодателей"""
    list_id = []
    for item in employers_list:
        for key in item.keys():
            if key == "employer_id":
                list_id.append(item[key])
    return list_id


def get_name_employers(employers_list: list[dict]) -> list:
    """Функция получения id работодателей"""
    list_name = []
    for item in employers_list:
        for key in item.keys():
            if key == "employer_name":
                list_name.append(item[key])
    return list_name


if __name__ == "__main__":
    employers = [
        {
            "employer_id": "1942330",
            "employer_name": "Пятёрочка",
            "url": "https://hh.ru/employer/1942330",
            "open_vacancies": 51108,
        },
        {
            "employer_id": "49357",
            "employer_name": "МАГНИТ, Розничная сеть",
            "url": "https://hh.ru/employer/49357",
            "open_vacancies": 34316,
        },
        {
            "employer_id": "78638",
            "employer_name": "Т-Банк",
            "url": "https://hh.ru/employer/78638",
            "open_vacancies": 15742,
        },
    ]
    # print(prints_a_greeting())
    # print()
    # gg = get_employers_id(employers)
    # print(gg)
    # print(type(get_employers_id(employers)))
    # print(len(gg))
    # print()
    # asd = get_name_employers(employers)
    # print(asd)
