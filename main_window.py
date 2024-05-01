from PyQt6.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem, QAbstractItemView, QHeaderView
from designer.main_window_d import Ui_MainWindow
from designer.employee_rating import Ui_Form
from ReadXlsx import ReadExcelPandas
from data_base import DataBase
from writer import Writer
import os


class TableWidget(QMainWindow):
    def __init__(self, employee_dict: dict):
        super(TableWidget, self).__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.__employee_dict = employee_dict

        self.table_widget = self.ui.tableWidget

    def set_table_widget(self):
        """
        Заполняет таблицу данными из self.__employee_dict.
        :return:
        """
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(
            ["Место", "Фамилия", "Итоговая сумма баллов", "План/факт", "Руководитель",
             "Сдача в срок"])
        self.table_widget.horizontalHeader().setStyleSheet(
            "QHeaderView::section {background-color: rgb(63, 63, 63); color: white;}")
        self.table_widget.verticalHeader().setVisible(False)
        self.table_widget.setColumnWidth(0, 50)
        self.table_widget.setColumnWidth(1, 140)
        self.table_widget.setColumnWidth(2, 160)
        self.table_widget.setColumnWidth(3, 110)
        self.table_widget.setColumnWidth(4, 110)
        self.table_widget.setColumnWidth(5, 110)
        self.table_widget.horizontalHeader().setStretchLastSection(True)

        for row, (place, (surname, scores)) in enumerate(
                zip(range(1, len(self.__employee_dict) + 1), self.__employee_dict.items())):
            self.table_widget.insertRow(row)
            self.table_widget.setItem(row, 0, QTableWidgetItem(str(place)))
            self.table_widget.setItem(row, 1, QTableWidgetItem(surname))
            self.table_widget.setItem(row, 2, QTableWidgetItem(str(scores[3])))
            self.table_widget.setItem(row, 3, QTableWidgetItem(str(scores[0])))
            self.table_widget.setItem(row, 4, QTableWidgetItem(str(scores[1])))
            self.table_widget.setItem(row, 5, QTableWidgetItem(str(scores[2])))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.table_widget = None
        self.res_table_widget = None
        self.dialog_window = None
        self.reader_excel = None
        self.__employee_dict = {}
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_confirm_choice.setDisabled(True)
        self.ui.btn_save.setDisabled(True)

        self.ui.btn_select_a_file.clicked.connect(self.set_table_widget)
        self.ui.btn_confirm_choice.clicked.connect(self.show_res_table_widget)
        self.ui.btn_save.clicked.connect(self.save_result)
        self.ui.btn_exit.clicked.connect(self.close)

    def set_table_widget(self):
        """
        Заполняет таблицу QTableWidget выбранными excel файлами из диалогового окна.
        :return:
        """
        dialog_window = QFileDialog()
        file_names = dialog_window.getOpenFileNames(self, "Open File", "", "Excel Files (*.xlsx);")
        if file_names:
            self.table_widget = self.ui.tableWidget
            self.table_widget.setSortingEnabled(True)
            self.table_widget.resizeColumnsToContents()
            self.table_widget.horizontalHeader().setStretchLastSection(True)
            self.table_widget.horizontalHeader().setVisible(False)
            self.table_widget.verticalHeader().setVisible(False)
            self.table_widget.setShowGrid(False)
            self.table_widget.setColumnCount(2)
            self.table_widget.setColumnWidth(0, 40)
            self.table_widget.setRowCount(len(file_names[0]))
            row = 0
            for num, file in enumerate(file_names[0], start=1):
                self.table_widget.setItem(row, 0, QTableWidgetItem(str(num)))
                self.table_widget.setItem(row, 1, QTableWidgetItem(file))
                row += 1
            self.table_widget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
            self.ui.btn_confirm_choice.setDisabled(False)
            return self.table_widget

    def get_path_from_table_widget(self) -> list[str]:
        """
        Возвращает список путей к excel файлам.
        :return:
            list[str] список строк
        """
        path_list = []
        for row in range(self.table_widget.rowCount()):
            item = self.table_widget.item(row, 1)
            if item is not None:
                value = item.text()
                path_list.append(value)
        return path_list

    def get_path_list_table_widget(self):
        return self.get_path_from_table_widget()

    def pathname_concatenation(self, file_extension: str) -> str:
        """
        Преобразует список, содержащий путь или несколько путей до файлов, возвращает сокращённое имя файла.
        :param file_extension: str, расширение файла.
        :return:
            str: строка.
        """
        path_list = self.get_path_from_table_widget()
        if len(path_list) > 1:
            res_name = ''
            for path in path_list:
                index_slash = path.rindex('/')
                index_point = path.rindex('.')
                edit_path = path[index_slash + 1:index_point]
                res_name += edit_path + '_'
            return res_name + file_extension
        else:
            index_slash = path_list[0].rindex('/')
            index_point = path_list[0].rindex('.')
            edit_path = path_list[0][index_slash + 1:index_point] + file_extension
            return edit_path

    def get_data_frame(self):
        """
        Возвращает список, содержащий объекты класса pandas.core.frame.DataFrame, по путям до excel файлов.
        :return:
            list[df]: список, содержащий DataFrame.
        """
        path_list = self.get_path_list_table_widget()
        all_df = []
        for path in path_list:
            reader = ReadExcelPandas(path)
            reader.delete_row(0)
            df = reader.read_excel_file()
            all_df.append(df)
        return all_df

    def get_surname_list_from_df(self) -> list[list[str]]:
        """
        Возвращает список списка фамилий сотрудников из Excel файла.
        :return:
            list[list[str]]
        """
        path_list = self.get_path_list_table_widget()
        all_surname_list = []
        for path in path_list:
            reader = ReadExcelPandas(path)
            surname_list = reader.read_employee_surname_list()
            all_surname_list.append(surname_list)
        return all_surname_list

    @staticmethod
    def check_for_file_existence(path_to_file: str) -> bool:
        """
        Возвращает True если файл существует по данному пути и False если файл отсутствует по данному пути.
        :param path_to_file: str, путь до файла
        :return:
            bool
        """
        return os.path.exists(path_to_file)

    def create_db(self):
        """
        Создаёт базу данных, создаёт в ней таблицы 'supervisor', 'projects', 'employees', 'project_deadline' и заполняет
        их данными.
        :return:
        """
        name_db = self.pathname_concatenation('.db')
        all_surname_list = self.get_surname_list_from_df()

        all_df = self.get_data_frame()
        data_base = DataBase(name_db)
        data_base.create_directory()
        data_base.create_db()
        for i in range(len(all_df)):
            data_base.create_table_supervisor()
            data_base.create_table_projects()
            data_base.create_table_employees()
            data_base.create_table_project_deadline()
            data_base.insert_values_into_db(all_df[i], all_surname_list[i])
            self.get_point_employee_from_db()

    @staticmethod
    def calculate_values(lst: list[tuple]) -> int:
        """
        Возвращает число, обозначающее количество баллов по план/факт показателю.
        :param lst: список кортежей
        :return:
            int
        """
        result = []
        for item in lst:
            if not item[0] and not item[1]:
                result.append(0)
            else:
                first_val = item[0] if item[0] is not None else int(item[1]) * 2
                second_val = item[1] if item[1] is not None else 0
                result.append(int(first_val) - int(second_val))
        return sum(result)

    @staticmethod
    def flatten_nested_list(nested_list) -> list[list[str]]:
        """
        Преобразует список списков в список списка.
        :param nested_list: список списков
        :return:
            list[list[str]]
        """
        flat_list = []
        for sublist in nested_list:
            flat_list.extend(sublist)
        return [flat_list]

    def convert_to_dictionary(self, employee_lst: list[tuple]):
        """
        Преобразует список кортежей, в каждом из которых содержатся фамилии сотрудников и их баллы, к словарю,
        где ключи это фамилии, а значения - это список чисел.
        :param employee_lst: список кортежей
        :return:
        """
        for name, number in employee_lst:
            if name not in self.__employee_dict:
                self.__employee_dict[name] = [number]
            else:
                self.__employee_dict[name].append(number)

    def append_point(self, supervisor_list: list[tuple]):
        """
        Добавляет в значения словаря число
        :param supervisor_list: список кортежей
        :return:
        """
        supervisor_lst = [item[0] for item in supervisor_list]
        for supervisor in self.__employee_dict.keys():
            if supervisor in supervisor_lst:
                self.__employee_dict[supervisor].append(supervisor_lst.count(supervisor))
            else:
                self.__employee_dict[supervisor].append(0)

    def append_sum_point(self):
        """
        Добавляет к списку значения словаря число.
        :return:
        """
        for surname, point in self.__employee_dict.items():
            total_point = sum(point)
            point.append(total_point)

    def sort_dict_by_last_number(self):
        """
        Сортирует словарь по последнему индексу списка значения.
        :return:
        """
        self.__employee_dict = dict(sorted(self.__employee_dict.items(), key=lambda x: (x[1][-1]), reverse=True))

    def get_point_employee_from_db(self):
        """
        Заполняет self.__employee_dict данными из бд.
        :return:
        """
        self.__employee_dict = {}
        name_db = self.pathname_concatenation('.db')
        all_surname_list = self.get_surname_list_from_df()
        if len(all_surname_list) > 1:
            all_surname_list = self.flatten_nested_list(all_surname_list)

        if not self.check_for_file_existence('data_base/' + name_db):
            self.create_db()
        else:
            data_base = DataBase(name_db)
            data_base.create_db()
            points_employee = data_base.get_point_employee(*all_surname_list)

            points_all_employee_lst = []
            for point in points_employee:
                calc_points = self.calculate_values(point)
                points_all_employee_lst.append(calc_points)

            point_plus_employee_man_days = list(zip(all_surname_list[0][0::2], points_all_employee_lst))
            self.convert_to_dictionary(point_plus_employee_man_days)
            supervisor_list = data_base.get_supervisor_list()
            point_deadline_projects_supervisor_list = data_base.get_point_deadline_projects_supervisor()
            self.append_point(supervisor_list)
            self.append_point(point_deadline_projects_supervisor_list)
            self.append_sum_point()
            self.sort_dict_by_last_number()
            print(self.__employee_dict)

    def show_res_table_widget(self):
        """
        Выводит окно с итоговым рейтингом сотрудников.
        :return:
        """
        self.get_point_employee_from_db()
        self.res_table_widget = TableWidget(self.__employee_dict)
        self.res_table_widget.show()
        self.ui.btn_save.setDisabled(False)
        self.res_table_widget.set_table_widget()

    def save_result(self):
        writer_file = Writer(self.__employee_dict)
        file_name = self.pathname_concatenation('.txt')
        writer_file.write_to_file(file_name)

