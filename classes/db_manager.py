import psycopg2
from utils.config import config

class DBManager:
    """
        Класс для управления базой данных и выполнения запросов.
    """
    def __init__(self, db_name):
        """
                Инициализирует объект DBManager с именем базы данных.

                Параметры:
                    db_name (str): Название базы данных.
                """
        self.__db_name = db_name

    def __execute_query(self, query):
        """
                Выполняет SQL-запрос и возвращает результат.

                Параметры:
                    query (str): SQL-запрос.

                Возвращает:
                    list: Результат выполнения запроса в виде списка кортежей.
                """
        con_params = config()
        con_params['dbname'] = self.__db_name
        con = psycopg2.connect(**con_params)
        with con:
            with con.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        return result

    def get_companies_and_vacancies_count(self):
        """
               Получает список всех компаний и количество вакансий у каждой компании.

               Возвращает:
                   list: Список кортежей, где каждый кортеж содержит название компании и количество вакансий.
               """
        query = "SELECT employers.name, COUNT(vacancies.id) as vacancies_count " \
                "FROM employers LEFT JOIN vacancies ON employers.id = vacancies.employer " \
                "GROUP BY employers.name"
        return self.__execute_query(query)

    def get_all_vacancies(self):
        """
                Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.

                Возвращает:
                    list: Список кортежей, где каждый кортеж содержит название компании, название вакансии,
                    минимальную и максимальную зарплату и ссылку на вакансию.
                """
        query = "SELECT employers.name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.link " \
                "FROM vacancies " \
                "JOIN employers ON vacancies.employer = employers.id"
        return self.__execute_query(query)

    def get_avg_salary(self):
        """
                Получает среднюю зарплату по всем вакансиям.

                Возвращает:
                    float: Средняя зарплата.
                """
        query = "SELECT AVG((vacancies.salary_from + vacancies.salary_to) / 2) as avg_salary " \
                "FROM vacancies"
        return self.__execute_query(query)[0][0]

    def get_vacancies_with_higher_salary(self):
        """
               Получает список всех вакансий с зарплатой выше средней по всем вакансиям.

               Возвращает:
                   list: Список кортежей, где каждый кортеж содержит название компании, название вакансии,
                   минимальную и максимальную зарплату и ссылку на вакансию.
               """
        avg_salary = self.get_avg_salary()
        query = f"SELECT employers.name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.link " \
                f"FROM vacancies " \
                f"JOIN employers ON vacancies.employer = employers.id " \
                f"WHERE (vacancies.salary_from + vacancies.salary_to) / 2 > {avg_salary}"
        return self.__execute_query(query)

    def get_vacancies_with_keyword(self, keyword):
        """
                Получает список всех вакансий, в названии которых содержится заданное ключевое слово.

                Параметры:
                    keyword (str): Ключевое слово для поиска в названиях вакансий.

                Возвращает:
                    list: Список кортежей, где каждый кортеж содержит название компании, название вакансии,
                    минимальную и максимальную зарплату и ссылку на вакансию.
                """
        query = f"SELECT employers.name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.link " \
                f"FROM vacancies " \
                f"JOIN employers ON vacancies.employer = employers.id " \
                f"WHERE vacancies.name ILIKE '%{keyword}%'"
        return self.__execute_query(query)

