from PyQt6.QtWidgets import QMainWindow, QFileDialog, QTableWidgetItem, QAbstractItemView
from designer.main_window_d import Ui_MainWindow
from ReadXlsx import ReadExcelPandas
from data_base import DataBase
import os


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.table_widget = None
        self.dialog_window = None
        self.reader_excel = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.btn_confirm_choice.setDisabled(True)
        self.ui.btn_save.setDisabled(True)

        self.ui.btn_select_a_file.clicked.connect(self.show_dialog)
        self.ui.btn_confirm_choice.clicked.connect(self.get_point_employee_man_days)
        self.ui.btn_exit.clicked.connect(self.close)

    def show_dialog(self):
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

    def get_path_from_table_widget(self):
        path_list = []
        for row in range(self.table_widget.rowCount()):
            item = self.table_widget.item(row, 1)
            if item is not None:
                value = item.text()
                path_list.append(value)
        return path_list

    def get_path_list_table_widget(self):
        return self.get_path_from_table_widget()

    def pathname_concatenation(self):
        path_list = self.get_path_from_table_widget()
        if len(path_list) > 1:
            res_name = ''
            for path in path_list:
                index_slash = path.rindex('/')
                index_point = path.rindex('.')
                edit_path = path[index_slash + 1:index_point]
                res_name += edit_path + '_'
            return res_name + '.db'
        else:
            index_slash = path_list[0].rindex('/')
            index_point = path_list[0].rindex('.')
            edit_path = path_list[0][index_slash + 1:index_point] + '.db'
            return edit_path

    def get_data_frame(self):
        path_list = self.get_path_list_table_widget()
        all_df = []
        for path in path_list:
            reader = ReadExcelPandas(path)
            reader.delete_row(0)
            df = reader.read_excel_file()
            all_df.append(df)
        return all_df

    def get_surname_list_from_df(self):
        path_list = self.get_path_list_table_widget()
        all_path_list = []
        for path in path_list:
            reader = ReadExcelPandas(path)
            surname_list = reader.read_employee_surname_list()
            all_path_list.append(surname_list)
        return all_path_list

    @staticmethod
    def check_for_file_existence(path_to_file: str):
        return os.path.exists(path_to_file)

    def create_db(self):
        name_db = self.pathname_concatenation()
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
            self.get_point_employee_man_days()

    @staticmethod
    def calculate_values(lst: list[tuple]) -> int:
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
    def flatten_nested_list(nested_list):
        flat_list = []
        for sublist in nested_list:
            flat_list.extend(sublist)
        return [flat_list]

    def get_point_employee_man_days(self):
        name_db = self.pathname_concatenation()
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
            print(all_surname_list[0][0::2])
            print(points_all_employee_lst)
            return points_all_employee_lst



