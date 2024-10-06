#  Основные настройки
#  Импорт библиотек
import logging
import os

from configparser import ConfigParser

#  Корневая директория проекта
ROOT_DIR = os.path.dirname(__file__)

#  Путь до готового файла
PATH_TO_FILE = os.path.join(ROOT_DIR, "data", "employers.json")

#  Путь к создаваемому файлу
NEW_PATH_TO_FILE = os.path.join(ROOT_DIR, "data")


#  Настройки для логгера
def setup_logger(name: str, log_file: str) -> logging.Logger:
    """Настойка логгера, включает метку времени,
    название модуля, уровень серьезности и сообщение,
    описывающее событие или ошибку, которая произошла."""
    logger = logging.getLogger(name)
    file_handler = logging.FileHandler(log_file, "w", encoding="UTF-8")
    file_formatter = logging.Formatter("%(asctime)s - %(filename)s - %(levelname)s: %(message)s")
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)
    logger.setLevel(logging.INFO)
    return logger


def config(filename="database.ini", section="postgresql"):
    # create a parser
    parser = ConfigParser()
    # read config file
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        # print(params)
        # db = dict(params)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception("Section {0} is not found in the {1} file.".format(section, filename))
    return db


if __name__ == "__main__":
    print(ROOT_DIR)
    print()
    print(PATH_TO_FILE)
    print()
    print(NEW_PATH_TO_FILE)
    print()
    print(config())
