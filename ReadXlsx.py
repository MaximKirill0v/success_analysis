import pandas as pd


class ReadExcelPandas:
    def __init__(self, file_path: str):
        self.df = pd.read_excel(file_path)

    def read_excel_file(self) -> pd.DataFrame:
        """
        Читает excel файл и возвращает DataFrame
        :return:
            pd.DataFrame
        """
        return self.df

    def delete_row(self, index: int):
        """
        Удаляет строку из DataFrame по заданному индексу.
        :param index: int, индекс строки, которую надо удалить.
        :return:
        """
        self.df = self.df.drop(index).reset_index(drop=True)

    def read_employee_surname_list(self) -> list[str]:
        """
        Возвращает список с фамилиями сотрудников из шапки DataFrame.
        :return:
            list[str]
        """
        header = list(self.df.columns)[4:]
        return header

