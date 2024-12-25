import os
import sys
from pathlib import Path
from PySide6.QtCore import QFile,QTextStream


if getattr(sys, 'frozen', False):
    SYS_PATH = Path(sys.executable).parent
else:
    SYS_PATH = Path(__file__).resolve().parent.parent

THEME_PATH = ":/qss/dark.qss"
URL_PATH = os.path.join(SYS_PATH, 'web', 'model_2', 'index.html')


def getStyleSheetFromFile(file: QFile):
    """ get style sheet from qss file """
    f = QFile(file)
    f.open(QFile.ReadOnly)
    qss = str(f.readAll(), encoding='utf-8')
    f.close()
    return qss

def getStyleSheet(file: QFile):
    file = QFile(file)
    if not file.open(QFile.ReadOnly | QFile.Text):
        print("Cannot open file for reading:", file.errorString())
        return
    stream = QTextStream(file)
    styleSheet = stream.readAll()
    file.close()
    return styleSheet