import requests


class HHAPI:
    BASE_URL = "https://api.hh.ru"

    @staticmethod
    def get_employers_data(employer_ids):
        employers_data = []
        for employer_id in employer_ids:
            response = requests.get(f'{HHAPI.BASE_URL}/employers/{employer_id}')
            response.encoding = 'utf-8'
            if response.status_code == 200:
                employers_data.append(response.json())
        return employers_data

    @staticmethod
    def get_vacancies_data(employer_id):
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
