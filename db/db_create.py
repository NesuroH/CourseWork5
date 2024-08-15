import psycopg2


def create_database(dbname: str, user: str, password: str, host: str):
    """
    Создает базу данных
    """
    conn = psycopg2.connect(dbname='postgres', user=user, password=password, host=host)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute(f"DROP DATABASE IF EXISTS {dbname}")
        cur.execute(f"CREATE DATABASE {dbname}")
    conn.close()


def create_tables(dbname: str, user: str, password: str, host: str):
    """
    Задает параметры для создания таблиц
    """
    conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host)
    conn.autocommit = True
    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE employers (
                id SERIAL PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                url VARCHAR(255),
                description TEXT
            )
        """)
        cur.execute("""
            CREATE TABLE vacancies (
                id SERIAL PRIMARY KEY,
                employer_id INTEGER REFERENCES employers(id),
                name VARCHAR(255) NOT NULL,
                salary_from INTEGER,
                salary_to INTEGER,
                url VARCHAR(255),
                description TEXT
            )
        """)
    conn.close()
