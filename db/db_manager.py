import psycopg2
from typing import List, Tuple


class DBManager:
    """
    Класс для управления операциями с базой данных вакансий.

    Атрибуты:
        conn (psycopg2.extensions.connection): Объект соединения с базой данных PostgreSQL.
    """

    def __init__(self, dbname: str, user: str, password: str, host: str):
        """
        Инициализирует объект DBManager и устанавливает соединение с базой данных.

        Параметры:
            dbname (str): Имя базы данных.
            user (str): Имя пользователя базы данных.
            password (str): Пароль пользователя базы данных.
            host (str): Хост базы данных.
        """
        self.conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
        self.conn.autocommit = True

    def get_companies_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """
        Возвращает список компаний и количество вакансий в каждой компании.

        Возвращает:
            List[Tuple[str, int]]: Список кортежей, где каждый кортеж содержит имя компании и количество вакансий.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, COUNT(v.id) 
                FROM employers e
                LEFT JOIN vacancies v ON e.id = v.employer_id
                GROUP BY e.name
            """)
            return cur.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, str, int, int, str]]:
        """
        Возвращает список всех вакансий с информацией о компании, названии вакансии, зарплате и URL.

        Возвращает:
            List[Tuple[str, str, int, int, str]]: Список кортежей, где каждый кортеж содержит имя компании, название вакансии, минимальную зарплату, максимальную зарплату и URL вакансии.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, v.name, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.id
            """)
            return cur.fetchall()

    def get_avg_salary(self) -> float:
        """
        Возвращает среднюю зарплату по всем вакансиям.

        Возвращает:
            float: Средняя зарплата.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT AVG((salary_from + salary_to) / 2)
                FROM vacancies
                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
            """)
            return cur.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, str, int, int, str]]:
        """
        Возвращает список вакансий с зарплатой выше средней.

        Возвращает:
            List[Tuple[str, str, int, int, str]]: Список кортежей, где каждый кортеж содержит имя компании, название вакансии, минимальную зарплату, максимальную зарплату и URL вакансии.
        """
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
        """
        Возвращает список вакансий, содержащих заданное ключевое слово в названии.

        Параметры:
            keyword (str): Ключевое слово для поиска в названиях вакансий.

        Возвращает:
            List[Tuple[str, str, int, int, str]]: Список кортежей, где каждый кортеж содержит имя компании, название вакансии, минимальную зарплату, максимальную зарплату и URL вакансии.
        """
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT e.name, v.name, v.salary_from, v.salary_to, v.url
                FROM vacancies v
                JOIN employers e ON v.employer_id = e.id
                WHERE v.name ILIKE %s
            """, (f'%{keyword}%',))
            return cur.fetchall()

    def close(self):
        """
        Закрывает соединение с базой данных.
        """
        self.conn.close()