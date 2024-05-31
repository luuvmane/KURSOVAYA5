from utils.utils import create_database, create_tables, insert_data_in_tables
from classes.db_manager import DBManager
db_name = "course_work"
create_database(db_name)
create_tables(db_name)
insert_data_in_tables(db_name)


def main_menu():
    """
       Отображает главное меню с вариантами действий для пользователя.
       Пользователь может выбрать одно из пяти действий, каждое из которых вызывает определенный запрос к базе данных.
       """
    print("Выберите действие:")
    print("1. Получить список всех компаний и количество вакансий у каждой компании")
    print("2. Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию")
    print("3. Получить среднюю зарплату по вакансиям")
    print("4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям")
    print("5. Получить список всех вакансий, в названии которых содержатся переданные в метод слова")

def get_user_choice():
    """
       Запрашивает у пользователя выбор действия из главного меню.

       Возвращает:
           int: Номер выбранного действия (от 1 до 5).
       """
    while True:
        try:
            choice = int(input("Введите цифру выбранного действия: "))
            if choice in range(1, 6):
                return choice
            else:
                print("Пожалуйста, введите число от 1 до 5.")
        except ValueError:
            print("Пожалуйста, введите целое число.")

def display_data(choice, db):
    """
       Выполняет действие в зависимости от выбора пользователя и отображает соответствующие данные.

       Параметры:
           choice (int): Номер выбранного действия.
           db (DBManager): Экземпляр класса DBManager для взаимодействия с базой данных.
       """
    if choice == 1:
        companies_vacancies = db.get_companies_and_vacancies_count()
        print("\nСписок всех компаний и количество вакансий у каждой:")
        for company in companies_vacancies:
            print(f"Компания: {company[0]}, Количество вакансий: {company[1]}")
    elif choice == 2:
        all_vacancies = db.get_all_vacancies()
        print("\nСписок всех вакансий:")
        for vacancy in all_vacancies:
            print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата от: {vacancy[2]}, Зарплата до: {vacancy[3]}, Ссылка: {vacancy[4]}")
    elif choice == 3:
        avg_salary = db.get_avg_salary()
        print(f"\nСредняя зарплата по вакансиям: {avg_salary}")
    elif choice == 4:
        higher_salary_vacancies = db.get_vacancies_with_higher_salary()
        print("\nСписок всех вакансий с зарплатой выше средней:")
        for vacancy in higher_salary_vacancies:
            print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата от: {vacancy[2]}, Зарплата до: {vacancy[3]}, Ссылка: {vacancy[4]}")
    elif choice == 5:
        keyword = input("Введите ключевое слово для поиска вакансий: ")
        keyword_vacancies = db.get_vacancies_with_keyword(keyword)
        print(f"\nСписок всех вакансий с ключевым словом '{keyword}':")
        for vacancy in keyword_vacancies:
            print(f"Компания: {vacancy[0]}, Вакансия: {vacancy[1]}, Зарплата от: {vacancy[2]}, Зарплата до: {vacancy[3]}, Ссылка: {vacancy[4]}")

def main():
    """
        Основная функция программы. Инициализирует соединение с базой данных и предоставляет пользователю интерфейс для выполнения различных действий.
        """
    db = DBManager("course_work")
    while True:
        main_menu()
        choice = get_user_choice()
        display_data(choice, db)
        continue_choice = input("Хотите выполнить еще одно действие? (да/нет): ")
        if continue_choice.lower() != 'да':
            break

if __name__ == "__main__":
    main()
