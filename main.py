from db.db_create import create_database, create_tables
from db.db_manager import DBManager
from vacancies.vacancy_manager import VacancyManager

def main():
    dbname = "course"
    user = "postgres"
    password = "nesuroHaki07"
    host = "localhost"

    create_database(dbname, user, password, host)
    create_tables(dbname, user, password, host)

    db_manager = DBManager(dbname, user, password, host)
    vacancy_manager = VacancyManager(db_manager)

    employer_ids = [9498120, 78638, 3529, 3127, 2115595, 41862, 9394111, 2392338, 373146, 2014495]  # Замените на реальные ID компаний
    vacancy_manager.load_data(employer_ids)

    print(db_manager.get_companies_and_vacancies_count())
    print(db_manager.get_all_vacancies())
    print(db_manager.get_avg_salary())
    print(db_manager.get_vacancies_with_higher_salary())
    print(db_manager.get_vacancies_with_keyword("разработчик"))

    db_manager.close()

if __name__ == "__main__":
    main()