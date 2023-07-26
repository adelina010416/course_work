import requests

from api.abstract_api import VacancyAPI
from constants import secret_key


class SuperJobAPI(VacancyAPI):
    """Класс для работы с API superjob.ru"""
    def get_all_vacancies(self, keyword, amount=100, field=1, salary=None):
        """
        Возвращает список вакансий по заданным параметрам
        Args:
            :keyword ключевые слова для поиска вакансий str
            :amount кол-во вакансий int
            :field поле (название/описание вакансии), в котором ищутся ключевые слова int
            :salary заработная плата int
        :return
            :result список словарей, содержащих данные вакансий
        """
        headers = {'X-Api-App-Id': secret_key}
        if field == 2:
            field = 10
        if salary:
            result = requests.get(f'https://api.superjob.ru/2.0/vacancies/?'
                                  f'keywords%5B1%5D%5Bsrws%5D={field}'
                                  f'&keywords%5B1%5D%5Bkeys%5D={keyword}'
                                  f'&count=100'
                                  f'&payment_from={int(salary)}',
                                  headers=headers)
        else:
            result = requests.get(f'https://api.superjob.ru/2.0/vacancies/?'
                                  f'keywords%5B1%5D%5Bsrws%5D={field}'
                                  f'&keywords%5B1%5D%5Bkeys%5D={keyword}'
                                  f'&count=100',
                                  headers=headers)
        return result.json()['objects'][:amount]

    def prepare_vacancies(self, keyword, amount=100, field=1, salary=None):
        vacancies_data = self.get_all_vacancies(keyword, amount, field, salary)
        prepared_vacancies = []
        for vacancy in vacancies_data:
            prepared_vacancy = {'profession': vacancy['profession'],
                                'link': vacancy['link'],
                                'salary': {
                                    'from': vacancy['payment_from'],
                                    'to': vacancy['payment_to'],
                                    'currency': vacancy['currency']
                                },
                                'address': vacancy['address']}
            if vacancy['candidat']:
                try:
                    prepared_vacancy['description'] = f"{vacancy['candidat'][:400]}..."
                except IndexError:
                    prepared_vacancy['description'] = f"{vacancy['candidat']}..."
            else:
                prepared_vacancy['description'] = ''
            prepared_vacancies.append(prepared_vacancy)
        return prepared_vacancies
