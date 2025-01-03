# coding:utf-8
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QHBoxLayout,QFileDialog
from qfluentwidgets import IconWidget, TextWrap,PushButton,InfoBar,InfoBarPosition
from app.common.style_sheet import StyleSheet

"""
1.窗口大小设置
2.控件初始化设置
3.控件大小以及控件布局
4.控件样式
5.控件槽函数功能
"""


class BriefCardBase(QFrame):

    def __init__(self, icon, title, content, parent=None):
        super().__init__(parent=parent)
        self.setFixedHeight(150)
        self.iconWidget = IconWidget(icon, self)
        self.titleLabel = QLabel(title, self)
        self.contentLabel = QLabel(TextWrap.wrap(content, 64, False)[0], self)

        self.__initWidget()

    def __initWidget(self):
        self.iconWidget.setFixedSize(120, 120)

        self.hBoxLayout = QHBoxLayout(self)
        self.vBoxLayout = QVBoxLayout()

        self.vBoxLayout.setSpacing(6)
        self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addWidget(self.contentLabel)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignVCenter)

        self.hBoxLayout.setSpacing(20)
        self.hBoxLayout.setContentsMargins(16, 0, 16, 0)

        self.hBoxLayout.addWidget(self.iconWidget, 1)
        self.hBoxLayout.addLayout(self.vBoxLayout, 1)
        self.hBoxLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.titleLabel.setObjectName('titleLabel')
        self.contentLabel.setObjectName('contentLabel')
        StyleSheet.BRIEF_CARD.apply(self)



if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    from qfluentwidgets import setTheme, Theme
    from app.recource import resource_rc

    setTheme(Theme.LIGHT)
    app = QApplication(sys.argv)
    w = BriefCardBase(
        icon=':/images/nuitka.png',
        title='Nuitka Tool',
        content=' Nuitka 是一个 Python 编译器。 Nuitka 的主要功能是将 Python 代码转换成 C 语言代码，再编译成机器代码，从而提高程序的运行效率。')
    w.show()
    app.exec()
