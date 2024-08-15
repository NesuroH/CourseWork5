import pytest
from unittest.mock import MagicMock, patch
from typing import List, Dict

# Adjust the import paths based on your project structure
from vacancies.vacancy_manager import VacancyManager, HHAPI
from db.db_manager import DBManager  # Assuming your DBManager class is in a file named dbmanager.py

# Mock data for testing
mock_employers_data = [
    {
        'id': '1',
        'name': 'Company A',
        'site_url': 'http://companya.com',
        'description': 'Description A'
    },
    {
        'id': '2',
        'name': 'Company B',
        'site_url': 'http://companyb.com',
        'description': 'Description B'
    }
]

mock_vacancies_data = [
    {
        'name': 'Vacancy 1',
        'salary': {'from': 50000, 'to': 70000},
        'alternate_url': 'http://example.com/1',
        'snippet': {'responsibility': 'Responsibility 1'}
    },
    {
        'name': 'Vacancy 2',
        'salary': {'from': 60000, 'to': 80000},
        'alternate_url': 'http://example.com/2',
        'snippet': {'responsibility': 'Responsibility 2'}
    }
]

@pytest.fixture
def db_manager():
    with patch('psycopg2.connect') as mock_connect:
        mock_conn = MagicMock()
        mock_cursor = mock_conn.cursor.return_value
        mock_cursor.__enter__.return_value = mock_cursor
        mock_cursor.__exit__.return_value = None
        mock_connect.return_value = mock_conn
        db_manager = DBManager(dbname='test_db', user='test_user', password='test_pass', host='test_host')
        yield db_manager
        db_manager.close()

@pytest.fixture
def vacancy_manager(db_manager):
    return VacancyManager(db_manager)

@patch.object(HHAPI, 'get_employers_data', return_value=mock_employers_data)
@patch.object(HHAPI, 'get_vacancies_data', return_value=mock_vacancies_data)
def test_load_data(mock_get_employers_data, mock_get_vacancies_data, vacancy_manager):
    vacancy_manager.insert_employer = MagicMock(return_value=1)
    vacancy_manager.insert_vacancy = MagicMock()

    employer_ids = ['1', '2']
    vacancy_manager.load_data(employer_ids)

    assert vacancy_manager.insert_employer.call_count == len(mock_employers_data)
    assert vacancy_manager.insert_vacancy.call_count == len(mock_employers_data) * len(mock_vacancies_data)

def test_insert_employer(vacancy_manager, db_manager):
    employer = mock_employers_data[0]
    expected_id = 1
    db_manager.conn.cursor().fetchone.return_value = (expected_id,)

    result = vacancy_manager.insert_employer(employer)
    assert result == expected_id

def test_insert_vacancy(vacancy_manager, db_manager):
    vacancy = mock_vacancies_data[0]
    employer_id = 1

    vacancy_manager.insert_vacancy(vacancy, employer_id)
    db_manager.conn.cursor().execute.assert_called_once_with("""
        INSERT INTO vacancies (employer_id, name, salary_from, salary_to, url, description)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (employer_id, vacancy['name'], vacancy['salary']['from'], vacancy['salary']['to'], vacancy['alternate_url'],
          vacancy['snippet']['responsibility']))

def test_get_employers_data():
    employer_ids = ['1', '2']
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = mock_employers_data
        mock_get.return_value = mock_response

        result = HHAPI.get_employers_data(employer_ids)
        assert result == mock_employers_data

def test_get_vacancies_data():
    employer_id = '1'
    with patch('requests.get') as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'items': mock_vacancies_data, 'pages': 1}
        mock_get.return_value = mock_response

        result = HHAPI.get_vacancies_data(employer_id)
        assert result == mock_vacancies_data
