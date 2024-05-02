from PyQt6.QtWidgets import QApplication
from window_qt import MainWindow
import sys


def execute_application():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == '__main__':
    execute_application()
