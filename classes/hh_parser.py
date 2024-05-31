import requests


class HHParser:
    """
       Класс для парсинга данных с сайта hh.ru.
       """

    @staticmethod
    def __get_response():
        """
               Выполняет запрос к API hh.ru для получения списка работодателей.

               Возвращает:
                   list: Список работодателей, каждый из которых представлен в виде словаря.
               """
        params = {"sort_by": "by_vacancies_open", "per_page": 10}
        response = requests.get("https://api.hh.ru/employers", params=params)
        if response.status_code == 200:
            return response.json()["items"]

    def get_employers(self):
        """
               Получает список работодателей с сайта hh.ru.

               Возвращает:
                   list: Список работодателей, каждый из которых представлен в виде словаря с ключами "id" и "name".
               """
        data = self.__get_response()
        employers = []
        for employer in data:
            employers.append({"id": employer["id"], "name": employer["name"]})
        return employers

    def get_vacancies(self):
        """
                Получает список вакансий от всех работодателей, полученных методом get_employers.

                Возвращает:
                    list: Список вакансий, каждая из которых представлена в виде словаря с ключами "id", "name",
                    "link", "salary_from", "salary_to" и "employer".
                """
        employers = self.get_employers()
        vacancies = []
        for employer in employers:
            params = {"employer_id": employer["id"]}
            response = requests.get("https://api.hh.ru/vacancies", params=params)
            if response.status_code == 200:
                filtered_vacancies = self.__filter_vacancies(response.json()["items"])
                vacancies.extend(filtered_vacancies)
        return vacancies

    @staticmethod
    def __filter_vacancies(vacancies):
        """
               Фильтрует список вакансий, извлекая необходимую информацию.

               Параметры:
                   vacancies (list): Список вакансий, каждая из которых представлена в виде словаря.

               Возвращает:
                   list: Отфильтрованный список вакансий, каждая из которых представлена в виде словаря с ключами "id",
                   "name", "link", "salary_from", "salary_to" и "employer".
               """
        filtered_vacancies = []
        for vacancy in vacancies:
            if vacancy["salary"] is None:
                salary_from = 0
                salary_to = 0
            else:
                salary_from = vacancy["salary"]["from"] if vacancy["salary"]["from"] else 0
                salary_to = vacancy["salary"]["to"] if vacancy["salary"]["to"] else 0
            filtered_vacancies.append({
                "id": vacancy["id"],
                "name": vacancy["name"],
                "link": vacancy["alternate_url"],
                "salary_from": salary_from,
                "salary_to": salary_to,
                "employer": vacancy["employer"]["id"]
            })
        return filtered_vacancies


