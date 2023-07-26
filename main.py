from api.hh_api import HeadHunterAPI
from api.superjob_api import SuperJobAPI
from constants import file_formats
from files.download_csv import DownloadCSV
from files.download_json import DownloadJSON
from files.download_txt import DownloadTXT
from vacancies.vacancies import Vacancy

hh_api = HeadHunterAPI()
sj_api = SuperJobAPI()
params = {}
platforms = ['headhunter', 'superjob']


def say_hello():
    """Выводит в консоль приветствие и список возможных команд"""
    print('Добро пожаловать!\n'
          'Чтобы начать поиск с параметрами по умолчанию, пожалуйста, введите "search".\n'
          '(поле поиска ключевых слов: название вакансии,\n'
          ' кол-во выводимых вакансий: 100,\n'
          ' зарплата от: не указана,\n'
          f' платформы: {", ".join(platforms)})\n\n'
          'Чтобы изменить параметры поиска, введите "params".\n'
          'Чтобы начать работу с файлом, введите "file"\n'
          'Чтобы выйти, введите "exit".')


def get_query():
    """
    Определяет запрос пользователя и вызывает соответствующие функции (главное меню приложения)
    Возможные команды: search, params, file, exit
    """
    while True:
        user_query = input('Введите команду: ').lower()
        if user_query == 'search':
            search()
        elif user_query == 'params':
            set_params(params, platforms)
        elif user_query == 'file':
            name, f_format = prepare_file_data()
            while True:
                user_file_query = input('Чтобы записать в файл вакансии, введите "write"\n'
                                        'Чтобы удалить вакансии из файла, введите "delete"\n'
                                        'Чтобы вывести на экран содержимое файла, введите "read"\n'
                                        'Чтобы выйти из режима работы с файлом, введите "exit"\n')
                if user_file_query == 'write' or user_file_query == 'delete':
                    vacs = get_vacancies_ids()
                    vacs_list = []
                    if user_file_query == 'write':
                        for vid in vacs:
                            for vac in Vacancy.all_vacancies():
                                if vid in vac.link:
                                    vacs_list.append(vac)
                        f_format.add(name, vacs_list)
                    if user_file_query == 'delete':
                        f_format.delete(name, vacs)
                elif user_file_query == 'read':
                    print(f_format.get_data(name))
                elif user_file_query == 'exit':
                    break
                else:
                    print("Команда не распознана. Пожалуйста, повторите запрос.")
        elif user_query == 'exit':
            break
        else:
            print("Команда не распознана. Пожалуйста, повторите запрос.")


def search():
    """Находит вакансии по заданным ключевым словам и выводит их в консоль"""
    while True:
        key_words = input('Пожалуйста, введите ключевые слова для поиска\n'
                          'или пустую строку, чтобы выйти из режима поиска.\n')
        if key_words == '':
            break
        Vacancy.delete_vacancies()
        params['keyword'] = key_words
        if 'headhunter' in platforms:
            hh_vacs = hh_api.prepare_vacancies(**params)
            Vacancy.add_vacancies(hh_vacs)
        if 'superjob' in platforms:
            sj_vacs = sj_api.prepare_vacancies(**params)
            Vacancy.add_vacancies(sj_vacs)
        [print(vac) for vac in Vacancy.all_vacancies()]


def set_params(f_params, f_platforms):
    """
    Настраивает параметры поиска (поля для поиска, кол-во вакансий, з/п, платформы для поиска)
    :param f_params: словарь с уже установленными параметрами dict
    :param f_platforms: список платформ list
    :return: обновлённые словарь с параметрами и список платформ
    """
    messages = ['Введите "1", если хотите искать ключевые слова в названии вакансии.\n'
                'Введите "2", если хотите искать ключевые слова в описании вакансии.\n',
                'Введите желаемое кол-во вакансий (максимальное кол-во 100).\n',
                'Введите минимальную зарплату (з/п от ...)\n'
                'Или нажмите "enter", чтобы оставить значение по умолчанию\n',
                'Введите "h", если хотите искать вакансии по hh.ru\n'
                'Введите "s", если хотите искать вакансии по superjob.ru\n'
                'Нажмите "enter", если хотите искать вакансии на обеих платформах.\n']
    new_params = []
    f_platforms[:] = []

    for i in range(len(messages)):
        while True:
            data = input(messages[i])
            if i != 3 and data != '':
                try:
                    data = int(data)
                except ValueError:
                    print('Недопустимый ввод. Введите число.')
                    continue
            if i == 0 and data not in [1, 2]:
                print('Недопустимый ввод. Введите "1" или "2"')
            elif i == 1 and data not in range(1, 101):
                print('Недопустимый ввод. Введите число не больше 100.')
            elif i == 3 and data not in ['h', 's', '']:
                print('Недопустимый ввод. Введите "h" / "s" / "".')
            else:
                new_params.append(data)
                break

    f_params['field'] = new_params[0]
    if new_params[2] != '':
        f_params['salary'] = new_params[2]
    else:
        f_params['salary'] = None

    if new_params[3] == 'h':
        f_platforms.append('headhunter')
    elif new_params[3] == 's':
        f_platforms.append('superjob')
    else:
        f_platforms[:] = ['headhunter', 'superjob']

    if not len(f_platforms) % 2 and not new_params[1] % 2:
        f_params['amount'] = new_params[1] // 2
    elif not len(f_platforms) % 2 and new_params[1] % 2:
        f_params['amount'] = new_params[1] // 2 + 1
    else:
        f_params['amount'] = new_params[1]
    return f_params, f_platforms


def prepare_file_data():
    """
    Принимает имя и формат файла, создаёт экземпляр соответствующего класса
    :return: имя файла и экземпляр класса для работы с файлом заданного формата
    """
    while True:
        name = input('Введите имя нового или существующего файла\n')
        file_format = input(f"Введите формат файла.\nВозможные варианты: {', '.join(file_formats)}\n")
        if file_format not in file_formats:
            print("Недопустимый формат файла")
        else:
            break

    if file_format == 'json':
        format_class = DownloadJSON()
    if file_format == 'txt':
        format_class = DownloadTXT()
    if file_format == 'csv':
        format_class = DownloadCSV()

    return name, format_class


def get_vacancies_ids():
    """
    Принимает строку из id вакансий, возвращает спасок из id в формате строки
    :return: спасок из id list
    """
    ids = input("Введите id вакансий, которые вы хотели бы записать/удалить, через пробел\n"
                "(id можно увидеть в ссылке на вакансию)\n").split(' ')
    for i in ids:
        while True:
            if not i.isdigit():
                ids.remove(i)
                new_i = input(f'Недопустимый ввод {i}.\nПожалуйста, повторите ввод желаемого id'
                              f' или нажмите "enter", чтобы пропустить его.\n')
                if new_i == '':
                    break
                i = new_i
            else:
                break
    return ids


if __name__ == '__main__':
    say_hello()
    get_query()
