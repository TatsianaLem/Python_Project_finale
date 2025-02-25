import pymysql
import logging
from pymysql.cursors import DictCursor


class DBConnection:
    """
        Класс для управления соединением с базой данных.
        Поддерживает подключение, выполнение запросов и логирование.
    """
    def __init__(self, dbconfig: dict, log_file: str):
        self._dbconfig = dbconfig
        self._connection = None
        self._cursor = None
        self._setup_logging(log_file)
        self._connect()

    def _setup_logging(self, log_file: str):
        if not logging.getLogger().hasHandlers():
            logging.basicConfig(filename=log_file, level=logging.INFO,
                                format="%(asctime)s - %(levelname)s - %(message)s")

    def _connect(self):
        """Создаёт подключение к базе данных и курсор."""
        try:
            self._connection = pymysql.connect(**self._dbconfig, cursorclass=DictCursor)
            self._cursor = self._connection.cursor()
        except pymysql.Error as e:
            logging.error(f"Ошибка подключения к БД: {e}")
            self._connection = None

    def execute_query(self, query: str, params=None):
        """Выполняет SQL-запрос и возвращает результат (если есть)."""
        if not self._connection or not self._connection.open:
            logging.warning("Соединение отсутствует, пытаемся переподключиться...")
            self._connect()

        if not self._connection:
            logging.error("Не удалось восстановить соединение с БД.")
            return None

        self.log_query(query)
        try:
            with self._connection.cursor() as cursor:
                cursor.execute(query, params)
                if query.strip().upper().startswith("SELECT"):
                    return cursor.fetchall()  # Возвращаем данные
                self._connection.commit()
        except pymysql.Error as e:
            logging.error(f"Ошибка выполнения запроса: {e}")
            self._connection.rollback()

    def log_query(self, query: str):
        logging.info(f"SQL Query: {query}")

    def get_connection(self):
        if not self._connection or not self._connection.open:
            self._connect()
        return self._connection

    def get_cursor(self):
        """Возвращает новый курсор для каждого вызова."""
        if not self._connection or not self._connection.open:
            self._connect()
        return self._connection.cursor() if self._connection else None

    def close(self):
        """Закрывает соединение с базой данных."""
        if self._cursor:
            self._cursor.close()
        if self._connection and self._connection.open:
            self._connection.close()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()