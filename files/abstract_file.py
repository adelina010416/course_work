from abc import ABC, abstractmethod


class DownloadVacancies(ABC):
    """Абстрактный класс для работы с файлами"""

    @staticmethod
    @abstractmethod
    def add(vacancy, file_name):
        pass

    @staticmethod
    @abstractmethod
    def get_data(filename):
        pass

    @staticmethod
    @abstractmethod
    def delete(filename, vacancy_id):
        pass
