import json
import os
from json import JSONDecodeError

from files.abstract_file import DownloadVacancies
from vacancies.vacancies import Vacancy


class DownloadJSON(DownloadVacancies):
    """Класс для работы с файлами .json"""

    @staticmethod
    def add(filename, vacancies: list):
        """
        Записывает список вакансий в файл с расширением csv
        :param filename: имя файла str
        :param vacancies: список вакансий list
        :return: str 'Готово!'
        """
        if os.path.exists(f'{filename}.json'):
            with open(f'{filename}.json', 'r', encoding='windows-1251') as file:
                try:
                    data = json.load(file)
                except JSONDecodeError:
                    data = []
        else:
            data = []

        for vac in vacancies:
            if not isinstance(vac, Vacancy):
                print(f'Не удалось записать в файл вакансию {vac}.')
                continue
            vacancy = {
                'profession': vac.profession,
                'salary': vac.salary,
                'address': vac.address,
                'description': vac.description,
                'link': vac.link
            }
            data.append(vacancy)

        with open(f'{filename}.json', 'w', encoding='windows-1251') as file:
            file.write(json.dumps(data, ensure_ascii=False, indent=4))
        return 'Готово!'

    @staticmethod
    def get_data(filename):
        """
        Выводит список вакансий из файла в консоль
        :param filename: имя файла str
        :return: список вакансий
        """
        try:
            with open(f'{filename}.json', 'r', encoding='windows-1251') as file:
                data = file.read()
            return data
        except FileNotFoundError:
            return 'Файл не найден'

    @staticmethod
    def delete(filename, vacancy_id: list):
        """
        Удаляет вакансии из файла по заданным id
        :param filename: имя файла str
        :param vacancy_id: список id вакансий list
        """
        try:
            with open(f'{filename}.json', 'r', encoding='windows-1251') as file:
                data = json.load(file)
        except FileNotFoundError:
            return 'Файл не найден'
        except JSONDecodeError:
            return 'Файл пуст'

        length_data = len(data)

        for vid in vacancy_id:
            for vacancy in data:
                if vid in vacancy['link']:
                    data.remove(vacancy)

        new_length = len(data)

        if length_data == new_length:
            return "Вакансия не найдена"
        with open(f'{filename}.json', 'w', encoding='windows-1251') as file:
            file.write(json.dumps(data, ensure_ascii=False, indent=4))
        return "Вакансия удалена"
