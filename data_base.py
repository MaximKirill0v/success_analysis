import sqlite3
from sqlite3 import Error


class DataBase:
    def __init__(self, path_to_db: str):
        self.__path_to_db = path_to_db
        self.__connection = None
        self.__cursor = None

    def create_db(self):
        self.__connection = sqlite3.connect(self.__path_to_db)
        print(f'Соединение установлено.{self.__path_to_db}')

    def close_db(self):
        self.__connection.close()
        print('Выход из ДБ')

    def __del__(self):
        self.__connection.close()
        print("Соединение закрыто.")

    def create_cursor(self):
        self.__cursor = self.__connection.cursor()
        print('курсор создан')

    def close_cursor(self):
        print('курсор закрыт')
        self.__cursor.close()

    def change_file_path(self, new_path: str):
        self.__path_to_db = new_path

