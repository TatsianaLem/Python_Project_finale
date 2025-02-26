import pymysql

from db_config import DBConfig
from query_manager import QueryHandler

# Очистка файла query_log.log перед запуском
#if os.path.exists("query_log.log"):
#    os.remove("query_log.log")


def task1(dbconfig, keyword):
    """ Выполняет поиск фильмов по ключевому слову и выводит результаты."""

    query_handler = QueryHandler(dbconfig)
    try:
        films = query_handler.get_films_by_keyword(keyword)
        if not films:
            print("Фильмы не найдены.")
            return
        for row in films:
            print(f"Title: {row.get('title')}")
            print(f"Description: {row.get('description')}")
            print(f"Year: {row.get('release_year')}")
            print("-" * 30)
    except pymysql.Error as e:
        print("SQLError", e)
    except Exception as e:
        print("Error", e)
    finally:
        query_handler.close()

def task2(dbconfig, genre, year):
    """ Выполняет поиск фильмов по жанру и году и выводит результаты."""

    query_handler = QueryHandler(dbconfig)
    try:
        films = query_handler.get_films_by_genre_and_year(genre, year)
        if not films:
            print("Фильмы не найдены.")
            return
        for row in films:
            print(f"Title: {row.get('title')}")
            print(f"Genre: {row.get('name')}")
            print(f"Year: {row.get('release_year')}")
            print("-" * 30)
    except pymysql.Error as e:
        print("SQLError", e)
    except Exception as e:
        print("Error", e)
    finally:
        query_handler.close()

if __name__ == "__main__":
    dbconfig = DBConfig()
    print(dbconfig.get_dbconfig())
    query_handler = QueryHandler(dbconfig.get_dbconfig())
    while True:
        print("\nВыберите действие: ")
        print("1. Поиск по ключевому слову")
        print("2. Поиск по жанру и году")
        print("3. Показать популярные запросы")
        print("4. Выход")

        choice = input("Введите номер действия: ")

        if choice == "1":
            keyword = input("Введите ключевое слово для поиска фильмов: ")
            task1(dbconfig.get_dbconfig(), keyword)

        elif choice == "2":
            genre = input("Введите жанр: ")
            try:
                year = int(input("Введите год: "))
                task2(dbconfig.get_dbconfig(), genre, year)
            except ValueError:
                print("Ошибка: Год должен быть числом.")

        elif choice == "3":
            query_handler.get_popular_queries()

        elif choice == '4':
            print("Выход из программы.")
            break

        else:
            print("Неверный выбор. Пожалуйста попробуйте снова.")