import datetime


def main():
    """Главная функция объединяет работу всех созданных функций."""

    data_now = datetime.date.today()
    datetime_now = datetime.datetime.now()
    time_now = datetime_now.time()
    print(data_now)
    print(time_now)


if __name__ == '__main__':
    main()
