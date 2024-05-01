import os


class Writer:
    def __init__(self, employee_dict: dict[str:[int]]):
        self.__employee_dict = employee_dict
        self.__directory_txt = 'text_file/'

    def create_directory(self):
        """
        Создаёт папку в нужной директории если её там нет.
        :return:
        """
        if not os.path.exists(self.__directory_txt):
            os.mkdir(self.__directory_txt)

    def write_file_txt(self, filename: str):
        """
        Записывает данные в txt файл.
        :param filename: str, название файла
        :return:
        """
        full_file_name = self.__directory_txt + filename
        self.create_directory()
        with open(full_file_name, 'w', encoding='utf-8') as f:
            for index, (name, values) in enumerate(self.__employee_dict.items(), 1):
                f.write(f"{index}. {name}\n")
                f.write(f"----общий балл:           {values[-1]}\n")
                f.write(f"----балл план/факт:       {values[0]}\n")
                f.write(f"----балл за руководителя: {values[1]}\n")
                f.write(f"----балл за сдачу в срок: {values[2]}\n")
