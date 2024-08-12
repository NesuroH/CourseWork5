from db.db_create import create_database, create_tables
from db.db_manager import DBManager
from vacancies.vacancy_manager import VacancyManager
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def main():
    dbname = "course"
    user = "postgres"
    password = "nesuroHaki07"
    host = "localhost"

    create_database(dbname, user, password, host)
    create_tables(dbname, user, password, host)

    db_manager = DBManager(dbname, user, password, host)
    vacancy_manager = VacancyManager(db_manager)

    employer_ids = [9498120, 78638, 3529, 3127, 2115595, 41862, 9394111, 2392338, 373146, 2014495]
    vacancy_manager.load_data(employer_ids)
    user_choice = int(input("Выберите желаемое действие:\n"
                            "1. Вывести список всех компаний и количество вакансий у каждой компании.\n"
                            "2. Вывести список всех вакансий c названием компании, названием вакансии, зарплатой и ссылкой на вакансию.\n"
                            "3. Вывести среднюю зарплату по вакансиям\n"
                            "4. Вывести список вакансий с зарплатой выше среднего\n"
                            "5. Найти вакансии по ключевому слову\n"))

    if user_choice == 1:
        print(db_manager.get_companies_and_vacancies_count())

    elif user_choice == 2:
        print(db_manager.get_all_vacancies())

    elif user_choice == 3:
        print(db_manager.get_avg_salary())

    elif user_choice == 4:
        print(db_manager.get_vacancies_with_higher_salary())

    elif user_choice == 5:
        key_word = input("Введите ключевое слово:\n")
        print(db_manager.get_vacancies_with_keyword(key_word))

    else:
        print("Нет такого действия")

    db_manager.close()


if __name__ == "__main__":
    main()
