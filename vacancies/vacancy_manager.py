from api.hh_api import HHAPI
from db.db_manager import DBManager


class VacancyManager:
    def __init__(self, db_manager: DBManager):
        self.db_manager = db_manager

    def load_data(self, employer_ids):
        employers_data = HHAPI.get_employers_data(employer_ids)
        for employer in employers_data:
            employer_id = self.insert_employer(employer)
            vacancies = HHAPI.get_vacancies_data(employer['id'])
            for vacancy in vacancies:
                self.insert_vacancy(vacancy, employer_id)

    def insert_employer(self, employer):
        with self.db_manager.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO employers (name, url, description)
                VALUES (%s, %s, %s)
                RETURNING id
            """, (employer['name'], employer['site_url'], employer['description']))
            return cur.fetchone()[0]

    def insert_vacancy(self, vacancy, employer_id):
        salary_from = vacancy['salary']['from'] if vacancy['salary'] and 'from' in vacancy['salary'] else None
        salary_to = vacancy['salary']['to'] if vacancy['salary'] and 'to' in vacancy['salary'] else None
        with self.db_manager.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO vacancies (employer_id, name, salary_from, salary_to, url, description)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (employer_id, vacancy['name'], salary_from, salary_to, vacancy['alternate_url'],
                  vacancy['snippet']['responsibility']))
