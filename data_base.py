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

    def create_table(self, name_table, column_names):
        with self.__connection:
            self.create_cursor()
            try:
                sql_request = f'''CREATE TABLE IF NOT EXISTS {name_table} ({", ".join(column_names)})'''
                self.__cursor.execute(sql_request)
                print(f'Таблица {name_table} создана.')
            except Error as e:
                print(e)
            finally:
                self.close_cursor()

    def create_table_supervisor(self):
        self.create_table('supervisor', ['ID INTEGER PRIMARY KEY', 'supervisor TEXT'])

    def create_table_projects(self):
        self.create_table('projects', ['ID INTEGER PRIMARY KEY', 'project_name TEXT UNIQUE', 'supervisor_ID INTEGER',
                                       'FOREIGN KEY (supervisor_ID) REFERENCES supervisor(ID)'])

    def create_table_employees(self):
        self.create_table('employees', ['ID INTEGER PRIMARY KEY', 'surname TEXT', 'plan TEXT', 'fact TEXT',
                                        'project_ID INTEGER', 'FOREIGN KEY (project_ID) REFERENCES projects(ID)'])

    def create_table_project_deadline(self):
        self.create_table('project_deadline', ['ID INTEGER PRIMARY KEY', 'planned_delivery_date INTEGER',
                                               'actual_delivery_date INTEGER', 'project_ID INTEGER',
                                               'FOREIGN KEY (project_ID) REFERENCES projects(ID)'])

