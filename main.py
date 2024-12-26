# coding:utf-8
import os
import sys

from PySide6.QtWidgets import QApplication

from app.view.main_window import MainWindow
from app.recource import resource_rc

if __name__ == '__main__':
    os.environ["QT_SCALE_FACTOR"] = "Auto"
    os.environ["QT_ENABLE_HIGHDPI_SCALING"] = "0"

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    sys.exit(app.exec())