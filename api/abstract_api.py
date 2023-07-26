from abc import ABC, abstractmethod


class VacancyAPI(ABC):
    """Абстрактный класс для подключения к API"""

    @abstractmethod
    def get_all_vacancies(self, keyword, amount, field, salary):
        pass

    @abstractmethod
    def prepare_vacancies(self, keyword, amount, field, salary):
        pass
