import requests


class Vacancy:
    """Класс для работы с вакансиями"""
    __all_vacancies = []

    def __init__(self, vacancies: dict):
        try:
            self._profession = vacancies['profession']
            self._link = vacancies['link']
            self._salary = vacancies['salary']
            self._description = vacancies['description']
            self._address = vacancies['address']
            self.__all_vacancies.append(self)
        except Exception:
            print(f'При обработке данных вакансии "{vacancies}" возникла ошибка')

    def __str__(self):
        payment = ''
        if self._salary['from']:
            payment += f'З/п от {self._salary["from"]} '
        if self._salary['to']:
            payment += f'до {self._salary["to"]} {self._salary["currency"]}'
        if not payment:
            payment = 'З/п не указана'
        return f'{self._profession}\n' \
               f'{payment}\n' \
               f'{self._address}\n' \
               f'{self._description}\n' \
               f'{self._link}\n'

    @property
    def profession(self):
        return self._profession

    @property
    def salary(self):
        return self._salary

    @property
    def address(self):
        return self._address

    @property
    def description(self):
        return self._description

    @property
    def link(self):
        return self._link

    @staticmethod
    def add_vacancies(vac_list):
        try:
            for vac in vac_list:
                Vacancy(vac)
        except TypeError:
            return False

    @classmethod
    def all_vacancies(cls):
        return cls.__all_vacancies

    @classmethod
    def delete_vacancies(cls):
        cls.__all_vacancies = []

    def get_rubles(self, currency: str, payment):
        """
        Переводит любую валюту в рубли
        :param currency: валюта str
        :param payment: сумма денег int
        :return: сумма в рублях int
        """
        course = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()['Valute']
        for cur in course.keys():
            if cur == currency:
                value = cur['Value']
                return value * int(payment)
        return 'Курс валюты не найден.'

    def prepare_comparison(self, other):
        """
        Проверяет возможность сравнения 2-х вакансий по з/п
        :return: список из 2-х экземпляров класса Vacancy
        """
        if not isinstance(other, Vacancy):
            return 'Ошибка! Сравнение невозможно.'
        payment1 = self._salary
        payment2 = other._salary
        for i in [payment1, payment2]:
            if type(i['from']) != int:
                try:
                    i['from'] = int(i['from'])
                except TypeError:
                    i['from'] = 0
            if i['currency'] != 'RUR' and i['currency'] != 'rub':
                i['from'] = self.get_rubles(i['currency'], i['from'])
                i['currency'] = 'RUR'
        return [payment1, payment2]

    def __lt__(self, other):
        payment1, payment2 = self.prepare_comparison(other)
        return payment1['from'] < payment2['from']

    def __gt__(self, other):
        payment1, payment2 = self.prepare_comparison(other)
        return payment1['from'] > payment2['from']

    def __le__(self, other):
        payment1, payment2 = self.prepare_comparison(other)
        return payment1['from'] <= payment2['from']

    def __ge__(self, other):
        payment1, payment2 = self.prepare_comparison(other)
        return payment1['from'] >= payment2['from']

    def __eq__(self, other):
        payment1, payment2 = self.prepare_comparison(other)
        return payment1['from'] == payment2['from']
