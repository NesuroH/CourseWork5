
import psycopg2
from typing import List, Tuple


class DBManager:
    def __init__(self, dbname: str, user: str, password: str, host: str):
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        self.conn.autocommit = True

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, COUNT(v.id) 
                FROM employers e
                LEFT JOIN vacancies v ON e.id = v.employer_id
                GROUP BY e.name
            """)
            return cur.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, int, int, str]]:
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, v.name, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.id
            """)
            return cur.fetchall()

    def get_avg_salary(self) -> float:
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG((salary_from + salary_to) / 2)
                FROM vacancies
                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
            """)
            return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, str, int, int, str]]:
        avg_salary = self.get_avg_salary()
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, v.name, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.id
                WHERE (v.salary_from + v.salary_to) / 2 > %s
            """, (avg_salary,))
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> List[Tuple[str, str, int, int, str]]:
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, v.name, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.id
                WHERE v.name ILIKE %s
            """, (f'%{keyword}%',))
            return cur.fetchall()

    def close(self):
        self.conn.close()
