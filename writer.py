import os


class Writer:
    def __init__(self, employee_dict: dict[str:[int]]):
        self.__employee_dict = employee_dict
        self.__directory = 'text_file/'

    def create_directory(self):
        """
        Создаёт папку в нужной директории если её там нет.
        :return:
        """
        if not os.path.exists(self.__directory):
            os.mkdir(self.__directory)

    def write_to_file(self, filename: str):
        full_file_name = self.__directory + filename
        self.create_directory()
        with open(full_file_name, 'w', encoding='utf-8') as f:
            for idx, (name, values) in enumerate(self.__employee_dict.items(), 1):
                f.write(f"{idx}. {name}\n")
                f.write(f"----общий балл:           {values[-1]}\n")
                f.write(f"----балл план/факт:       {values[0]}\n")
                f.write(f"----балл за руководителя: {values[1]}\n")
                f.write(f"----балл за сдачу в срок: {values[2]}\n")