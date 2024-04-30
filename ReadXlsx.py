import pandas as pd


class ReadExcelPandas:
    def __init__(self, file_path: str):
        self.df = pd.read_excel(file_path)

    def read_excel_file(self):
        return self.df

    def delete_row(self, index: int):
        self.df = self.df.drop(index).reset_index(drop=True)

    def read_employee_surname_list(self):
        header = list(self.df.columns)[4:]
        return header

