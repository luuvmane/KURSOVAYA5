import psycopg2
from utils.config import config

class DBManager:
    def __init__(self, db_name):
        self.__db_name = db_name

    def __execute_query(self, query):
        con_params = config()
        con_params['dbname'] = self.__db_name
        con = psycopg2.connect(**con_params)
        with con:
            with con.cursor() as cur:
                cur.execute(query)
                result = cur.fetchall()
        return result

    def get_companies_and_vacancies_count(self):
        query = "SELECT employers.name, COUNT(vacancies.id) as vacancies_count " \
                "FROM employers LEFT JOIN vacancies ON employers.id = vacancies.employer " \
                "GROUP BY employers.name"
        return self.__execute_query(query)

    def get_all_vacancies(self):
        query = "SELECT employers.name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.link " \
                "FROM vacancies " \
                "JOIN employers ON vacancies.employer = employers.id"
        return self.__execute_query(query)

    def get_avg_salary(self):
        query = "SELECT AVG((vacancies.salary_from + vacancies.salary_to) / 2) as avg_salary " \
                "FROM vacancies"
        return self.__execute_query(query)[0][0]

    def get_vacancies_with_higher_salary(self):
        avg_salary = self.get_avg_salary()
        query = f"SELECT employers.name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.link " \
                f"FROM vacancies " \
                f"JOIN employers ON vacancies.employer = employers.id " \
                f"WHERE (vacancies.salary_from + vacancies.salary_to) / 2 > {avg_salary}"
        return self.__execute_query(query)

    def get_vacancies_with_keyword(self, keyword):
        query = f"SELECT employers.name, vacancies.name, vacancies.salary_from, vacancies.salary_to, vacancies.link " \
                f"FROM vacancies " \
                f"JOIN employers ON vacancies.employer = employers.id " \
                f"WHERE vacancies.name ILIKE '%{keyword}%'"
        return self.__execute_query(query)

