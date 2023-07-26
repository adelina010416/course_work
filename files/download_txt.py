import os

from files.abstract_file import DownloadVacancies
from vacancies.vacancies import Vacancy


class DownloadTXT(DownloadVacancies):
    """Класс для работы с файлами .txt"""

    @staticmethod
    def add(filename, vacancies: list):
        """
        Записывает список вакансий в файл с расширением csv
        :param filename: имя файла str
        :param vacancies: список вакансий list
        :return: str 'Готово!'
        """
        result = ''

        if os.path.exists(f'{filename}.txt'):
            param = 'a'
        else:
            param = 'w'

        for vac in vacancies:
            if not isinstance(vac, Vacancy):
                print(f'Не удалось записать в файл вакансию {vac}.')
                continue
            payment = ''
            if vac.salary['from']:
                payment += f'З/п от {vac.salary["from"]} '
            if vac.salary['to']:
                payment += f'до {vac.salary["to"]} {vac.salary["currency"]}'
            if not payment:
                payment = 'З/п не указана'
            result += f'{vac.profession}\n' \
                      f'{payment}\n' \
                      f'{vac.address}\n' \
                      f'{vac.description}\n' \
                      f'{vac.link}\n\n'

        with open(f'{filename}.txt', param, encoding='windows-1251') as file:
            file.write(result)
        return 'Готово!'

    @staticmethod
    def get_data(filename):
        """
        Выводит список вакансий из файла в консоль
        :param filename: имя файла str
        :return: список вакансий
        """
        try:
            with open(f'{filename}.txt', 'r', encoding='windows-1251') as file:
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
            with open(f'{filename}.txt', 'r', encoding='windows-1251') as file:
                data = file.read()
        except FileNotFoundError:
            return 'Файл не найден'

        data = data.split('\n\n')
        length_data = len(data)

        for vid in vacancy_id:
            for vacancy in data:
                if vid in vacancy:
                    data.remove(vacancy)

        new_length = len(data)

        if length_data == new_length:
            return "Вакансия не найдена"
        with open(f'{filename}.txt', 'w', encoding='windows-1251') as file:
            file.write('\n\n'.join(data))
        return "Вакансия удалена"
