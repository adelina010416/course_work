import requests

from api.abstract_api import VacancyAPI


class HeadHunterAPI(VacancyAPI):
    """Класс для работы с API hh.ru"""

    def get_all_vacancies(self, keyword, amount=100, field='name', salary=None):
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
        if field == 1:
            field = 'name'
        if field == 2:
            field = 'description'
        params = {'text': keyword,
                  'per_page': amount,
                  'only_with_salary': 'true',
                  'search_field': field}

        if salary:
            try:
                params['salary'] = int(salary)
            except TypeError:
                print('Недопустимый ввод зарплаты.')

        response = requests.get('https://api.hh.ru/vacancies', params=params)
        result = response.json()['items']
        return result

    def prepare_vacancies(self, keyword, amount=100, field='name', salary=None):
        """
        Приводит словари с вакансиями к одному формату
        Args:
            :keyword ключевые слова для поиска вакансий str
            :amount кол-во вакансий int
            :field поле (название/описание вакансии), в котором ищутся ключевые слова int
            :salary заработная плата int
        :return
            :prepared_vacancies список словарей, содержащих данные вакансий
        """
        prepared_vacancies = []
        stop_marker = False

        while not stop_marker:
            fails = 0
            vacancies_data = self.get_all_vacancies(keyword, amount, field, salary)

            for vacancy in vacancies_data:
                try:
                    prepared_vacancy = {'profession': vacancy['name'],
                                        'link': vacancy['alternate_url'],
                                        'salary': {
                                            'from': vacancy['salary']['from'],
                                            'to': vacancy['salary']['to'],
                                            'currency': vacancy['salary']['currency']
                                        },
                                        'description': f'Требования: {vacancy["snippet"]["requirement"]}\n'
                                                       f'Обязанности: {vacancy["snippet"]["responsibility"]}'}
                    if vacancy['address']:
                        prepared_vacancy['address'] = vacancy['address']['raw']
                    else:
                        prepared_vacancy['address'] = 'адрес не указан'
                    prepared_vacancies.append(prepared_vacancy)
                except TypeError:
                    fails += 1

            if fails == 0:
                stop_marker = True
            else:
                amount = fails

        return prepared_vacancies
