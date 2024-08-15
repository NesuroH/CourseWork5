import requests


class HHAPI:
    """
    Класс для взаимодействия с API HeadHunter (hh.ru).

    Атрибуты:
        BASE_URL (str): Базовый URL для API HeadHunter.
    """

    BASE_URL = "https://api.hh.ru"

    @staticmethod
    def get_employers_data(employer_ids):
        """
        Получает данные о работодателях по их идентификаторам.

        Параметры:
            employer_ids (list): Список идентификаторов работодателей.

        Возвращает:
            list: Список данных о работодателях в формате JSON.
        """
        employers_data = []
        for employer_id in employer_ids:
            response = requests.get(f'{HHAPI.BASE_URL}/employers/{employer_id}')
            response.encoding = 'utf-8'
            if response.status_code == 200:
                employers_data.append(response.json())
        return employers_data

    @staticmethod
    def get_vacancies_data(employer_id):
        """
        Получает данные о вакансиях для заданного работодателя.

        Параметры:
            employer_id (str): Идентификатор работодателя.

        Возвращает:
            list: Список данных о вакансиях в формате JSON.
        """
        vacancies_data = []
        page = 0
        while True:
            response = requests.get(f'{HHAPI.BASE_URL}/vacancies?employer_id={employer_id}&page={page}')
            response.encoding = 'utf-8'
            if response.status_code == 200:
                data = response.json()
                vacancies_data.extend(data['items'])
                if data['pages'] - 1 == page:
                    break
                page += 1
            else:
                break
        return vacancies_data