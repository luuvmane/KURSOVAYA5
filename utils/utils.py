import psycopg2
from utils.config import config
from classes.hh_parser import HHParser

def create_database(db_name):
    # Получение конфигурации подключения
    params = config()
    print("Connection parameters:", params)

    # Подключение к базе данных postgres
    con = psycopg2.connect(**params)
    con.autocommit = True
    cur = con.cursor()
    # Удаление БД если существует
    cur.execute(f"DROP DATABASE IF EXISTS {db_name}")
    # Создание новой базы данных
    cur.execute(f"CREATE DATABASE {db_name}")
    cur.close()
    con.close()

def create_tables(db_name):
    con_params = config()
    con_params['dbname'] = db_name  # Добавляем dbname к параметрам подключения

    con = psycopg2.connect(**con_params)
    with con:
        with con.cursor() as cur:
            cur.execute("CREATE TABLE employers (id SERIAL PRIMARY KEY, name VARCHAR(150))")
            cur.execute("CREATE TABLE vacancies (id SERIAL PRIMARY KEY, name VARCHAR(150),"
                        "link VARCHAR(150), salary_from INTEGER, salary_to INTEGER,"
                        "employer INTEGER REFERENCES employers(id))")
    con.close()



def insert_data_in_tables(db_name):
    # Создаем экземпляр HHParser
    hh = HHParser()

    # Получаем список работодателей и вакансий
    employers = hh.get_employers()
    vacancies = hh.get_vacancies()

    # Получаем конфигурацию подключения к базе данных
    con_params = config()
    con_params['dbname'] = db_name  # Добавляем dbname к параметрам подключения

    # Подключаемся к базе данных
    con = psycopg2.connect(**con_params)
    with con:
        with con.cursor() as cur:
            # Вставляем данные работодателей в таблицу employers
            for employer in employers:
                cur.execute("INSERT INTO employers (id, name) VALUES (%s, %s)", (employer["id"], employer["name"]))
            # Вставляем данные вакансий в таблицу vacancies
            for vacancy in vacancies:
                cur.execute("INSERT INTO vacancies (id, name, link, salary_from, salary_to, employer) "
                            "VALUES (%s, %s, %s, %s, %s, %s)",
                            (vacancy["id"], vacancy["name"], vacancy["link"], vacancy["salary_from"],
                             vacancy["salary_to"], vacancy.get("employer")))  # Используем .get() для извлечения employer_id

    con.close()
