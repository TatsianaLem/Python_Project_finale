import logging
import json
import os
from db_connection import DBConnection
from sql_queries import FilmQueries

class QueryHandler(DBConnection):
    """ Инициализирует обработчик запросов. """
    def __init__(self, dbconfig, log_file='app.log', query_log_file='query_log.log', count_file='query_counts.json'):
        super().__init__(dbconfig, log_file)
        self.query_log_file = query_log_file
        self.count_file = count_file
        self.query_counts = self.load_query_counts()

    def log_query(self, query, params):
        """
            Логирует выполненный запрос, обновляет счетчики и сохраняет их.
        """
        param_str = ', '.join(map(str.strip, map(str, params)))

        self.query_counts[param_str] = self.query_counts.get(param_str, 0) + 1

        with open(self.query_log_file, 'a') as f:
            f.write(f"Params: ({param_str})\n")
            f.write(f"Total Execution for this Query: {self.query_counts.get(param_str)}\n\n")
        self.save_query_counts()

        print(f"Params: ({param_str})")
        print(f"Total Execution for this Query: {self.query_counts.get(param_str)}")

    def load_query_counts(self):
        """ Загружает данные о популярных запросах из JSON-файла. """
        if os.path.exists(self.count_file):
            with open(self.count_file, 'r') as f:
                try:
                    return json.load(f)
                except json.JSONDecodeError:
                    return {}
        return {}

    def save_query_counts(self):
        """ Сохраняет текущие популярные запросы в JSON-файл """
        with open(self.count_file, 'w') as f:
            json.dump(self.query_counts, f, indent=4)

    def get_popular_queries(self, top_n=5):
        """ Выводит top_n самых популярных запросов. """
        sorted_queries = sorted(self.query_counts.items(), key=lambda x: x[1], reverse=True)

        if not sorted_queries:
            print("Нет популярных запросов.")
            return []
        print("Самые популярные запросы (параметры):")

        for query, count in sorted_queries[:top_n]:
            print(f"Params: {query} | Total Execution for this Query: {count}")

    def get_all_films(self):
        """ Получает все фильмы из базы данных."""
        try:
            with self.get_cursor() as cursor:
                cursor.execute(FilmQueries.GET_ALL)
                return cursor.fetchall()
        except Exception as e:
            logging.error(f"Ошибка при получении всех фильмов: {e}")
            return []

    def get_films_by_keyword(self, keyword):
        """ Получает фильмы по ключевому слову """
        query, params = FilmQueries.get_films_by_keyword(keyword)
        self.log_query(query, params)
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                records = cursor.fetchall()
                return records
        except Exception as e:
            logging.error(f"Ошибка при получении фильмов по ключевому слову '{keyword}': {e}")
            return []

    def get_films_by_genre_and_year(self, genre: str, year: int):
        """ Получает фильмы по жанру и году """
        query, params = FilmQueries.get_films_by_genre_and_year(genre, year)
        self.log_query(query, params)
        try:
            with self.get_cursor() as cursor:
                cursor.execute(query, params)
                records = cursor.fetchall()
                #print("Выполнение запроса: ", records)
                return records
        except Exception as e:
            logging.error(f"Ошибка при получении фильмов по жанру '{genre}' и году '{year}' : {e}")
            return []
