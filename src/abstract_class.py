from abc import ABC, abstractmethod


class Parser(ABC):
    """Абстрактный класс по работе с API сервисом."""

    @abstractmethod
    def get_info_employers(self) -> None:
        pass

    @abstractmethod
    def get_vacancies_employer(self, employer_id) -> None:
        pass


class ReadWriteFile(ABC):
    """Абстрактный класс по чтению/записи файла."""

    @abstractmethod
    def read_new_vacancy_file(self):
        pass

    @abstractmethod
    def delete_file(self):
        pass
