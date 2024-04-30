import sqlite3
from sqlite3 import Error
import pandas as pd
import os


class DataBase:
    def __init__(self, path_to_db: str):
        self.__path_to_db = path_to_db
        self.__directory = 'data_base/'
        self.__connection = None
        self.__cursor = None

    def create_db(self):
        print(self.__directory + self.__path_to_db)
        self.__connection = sqlite3.connect(self.__directory + self.__path_to_db)
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

    def rename_directory(self, new_name: str):
        self.__directory = new_name

    def create_directory(self):
        if not os.path.exists(self.__directory):
            os.mkdir(self.__directory)

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
        self.create_table('projects', ['ID INTEGER PRIMARY KEY', 'project_name TEXT', 'supervisor_ID INTEGER',
                                       'FOREIGN KEY (supervisor_ID) REFERENCES supervisor(ID)'])

    def create_table_employees(self):
        self.create_table('employees', ['ID INTEGER PRIMARY KEY', 'surname TEXT', 'plan TEXT', 'fact TEXT',
                                        'project_ID INTEGER', 'FOREIGN KEY (project_ID) REFERENCES projects(ID)'])

    def create_table_project_deadline(self):
        self.create_table('project_deadline', ['ID INTEGER PRIMARY KEY', 'planned_delivery_date INTEGER',
                                               'actual_delivery_date INTEGER', 'project_ID INTEGER',
                                               'FOREIGN KEY (project_ID) REFERENCES projects(ID)'])

    def insert_values_into_db(self, data_frame: pd.DataFrame, surname_list: list):

        with self.__connection:
            self.create_cursor()
            try:
                for index, row in data_frame.iterrows():
                    self.__cursor.execute("INSERT INTO supervisor (supervisor) VALUES (?)", (row['Руководитель'],))
                    self.__cursor.execute(
                        "INSERT INTO projects (project_name, supervisor_ID) "
                        "VALUES (?, (SELECT ID FROM supervisor WHERE supervisor = ?))",
                        (row['Название проекта'], row['Руководитель']))

                    timestamp_plan = pd.Timestamp(row['Дата сдачи план.'])
                    unix_time_plan = int(timestamp_plan.timestamp())

                    timestamp_fact = pd.Timestamp(row['Дата сдачи факт.'])
                    unix_time_fact = int(timestamp_fact.timestamp())

                    self.__cursor.execute(
                        "INSERT INTO project_deadline (planned_delivery_date, actual_delivery_date, project_ID)"
                        "VALUES (?, ?, (SELECT ID FROM projects WHERE project_name = ?))",
                        (unix_time_plan, unix_time_fact, row['Название проекта']))

                    for surname in surname_list[0::2]:
                        self.__cursor.execute(
                            "INSERT INTO employees (surname, plan, fact, project_ID)"
                            "VALUES (?, ?, ?, (SELECT ID FROM projects WHERE project_name = ?))",
                            (surname, row[surname], row[surname + '.1'], row['Название проекта']))
            except Error:
                return False
            finally:
                print('До')
                self.__cursor.close()
                print('после')

    def get_point_employee(self, surname_list: list):
        with self.__connection:
            self.create_cursor()
            surname_point_lst = []
            try:
                for surname in surname_list[0::2]:
                    sql_request = f"""SELECT plan, fact FROM employees WHERE surname = '{surname}'"""
                    self.__cursor.execute(sql_request)
                    surname_point = self.__cursor.fetchall()
                    surname_point_lst.append(surname_point)
                return surname_point_lst
            except Error as e:
                print(e)
            finally:
                self.__cursor.close()

    def get_supervisor_list(self):
        with self.__connection:
            self.create_cursor()
            try:
                sql_request = f"""SELECT supervisor FROM supervisor"""
                self.__cursor.execute(sql_request)
                supervisor_list = self.__cursor.fetchall()
                return supervisor_list
            except Error as e:
                print(e)
            finally:
                self.__cursor.close()

    def get_point_deadline_projects_supervisor(self):
        with self.__connection:
            self.create_cursor()
            try:
                sql_request = f"SELECT supervisor.supervisor " \
                              f"FROM supervisor, project_deadline, projects " \
                              f"WHERE (project_deadline.planned_delivery_date >= project_deadline.actual_delivery_date) " \
                              f"AND projects.ID = project_deadline.project_ID " \
                              f"AND projects.supervisor_ID = supervisor.ID"
                self.__cursor.execute(sql_request)
                point_deadline_projects_supervisor_list = self.__cursor.fetchall()
                return point_deadline_projects_supervisor_list
            except Error as e:
                print(e)
            finally:
                self.__cursor.close()
