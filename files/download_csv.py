import csv
import os

from files.abstract_file import DownloadVacancies
from vacancies.vacancies import Vacancy


class DownloadCSV(DownloadVacancies):
    """Класс для работы с файлами .csv"""

    @staticmethod
    def add(file_name, vacancies: list):
        """
        Записывает список вакансий в файл с расширением csv
        :param file_name: имя файла str
        :param vacancies: список вакансий list
        :return: str 'Готово!'
        """
        columns = ["вакансия", "з/п от и до", "адрес", "описание", "ссылка"]
        if not os.path.exists(file_name):
            with open(file_name, mode='w', encoding='windows-1251') as file:
                file_writer = csv.writer(file, delimiter=";", lineterminator="\r")
                file_writer.writerow(columns)

        with open(file_name, mode='a', encoding='windows-1251') as file:
            file_writer = csv.DictWriter(file, delimiter=";", lineterminator="\r", fieldnames=columns)
            for vac in vacancies:
                if not isinstance(vac, Vacancy):
                    print(f'Не удалось записать в файл вакансию {vac}.')
                    continue
                description = vac.description.replace('\n', ' ')
                salary = f"{vac.salary['from']}-{vac.salary['to']} {vac.salary['currency']}"
                file_writer.writerow({
                    'вакансия': vac.profession,
                    'з/п от и до': salary,
                    'адрес': vac.address,
                    'описание': description,
                    'ссылка': vac.link
                })
        return 'Готово!'

    @staticmethod
    def get_data(filename):
        """
        Выводит список вакансий из файла в консоль
        :param filename: имя файла str
        :return: список вакансий str
        """
        try:
            with open(f'{filename}.csv', newline='', encoding='windows-1251') as file:
                reader = csv.reader(file)
                result = ''
                for row in reader:
                    result += f'{row}\n'
            return result
        except FileNotFoundError:
            return 'Файл не найден'

    @staticmethod
    def delete(filename, vacancy_id: list):
        """
        Удаляет вакансии из файла по заданным id
        :param filename: имя файла str
        :param vacancy_id: список id вакансий list
        """
        columns = ["вакансия", "з/п от и до", "адрес", "описание", "ссылка"]
        try:
            with open(f'{filename}.csv', encoding='windows-1251') as file:
                lines = file.readlines()[1:]
            for vid in vacancy_id:
                for i in lines:
                    if str(vid) in i:
                        lines.remove(i)
            with open(f'{filename}.csv', mode='w', encoding='windows-1251') as file:
                file_writer = csv.writer(file, delimiter=";", lineterminator="\r")
                file_writer.writerow(columns)
                file_writer = csv.DictWriter(file, delimiter=";", lineterminator="\r", fieldnames=columns)
                for line in lines:
                    line = line.split(';')
                    file_writer.writerow({
                        'вакансия': line[0],
                        'з/п от и до': line[1],
                        'адрес': line[2],
                        'описание': line[3],
                        'ссылка': line[4]
                    })
            return 'Вакансия удалена'
        except FileNotFoundError:
            return 'Файл не найден'
