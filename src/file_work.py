import json
import os
from abc import ABC
from typing import Any

from config import NEW_PATH_TO_FILE, PATH_TO_FILE
from src.abstract_class import ReadWriteFile


class JobFile(ReadWriteFile, ABC):
    """Класс по работе с JSON-файлами."""

    filename: str

    def __init__(self, filename: str):
        self.filename = filename
        self.path_file = os.path.join(NEW_PATH_TO_FILE, filename)

    @staticmethod
    def read_file() -> Any:
        """Читает данные из стандартного JSON-файла."""
        try:
            with open(PATH_TO_FILE, "r", encoding="UTF-8") as f:
                try:
                    # my_logger.info("Открытие файла")
                    data_file = json.load(f)
                    return data_file
                except json.JSONDecodeError:
                    # my_logger.error("Возникла ошибка при обработке файла! Неверный формат файла")
                    return []
        except FileNotFoundError:
            # my_logger.error("Файл не найден")
            return []

    def save_vacancy_file(self, vacancies: list[dict]) -> None:
        """Сохраняет данные в JSON-файл."""
        with open(self.path_file, "w", encoding="UTF-8") as f:
            json.dump(vacancies, f, ensure_ascii=False, indent=4)

    def read_new_vacancy_file(self) -> Any:
        """Читает данные из нового JSON-файла."""
        # print(self.path_file)
        with open(self.path_file, encoding="UTF-8") as f:
            data_file_new = json.load(f)
            return data_file_new

    def delete_file(self) -> None:
        """Удаление данных из нового JSON-файла."""
        open(self.path_file, "w").close()


if __name__ == "__main__":
    user_file = JobFile("employers.json")
    u = user_file.read_file()
    print(u)
    print(len(u))
    print(type(u))
