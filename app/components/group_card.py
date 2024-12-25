from PySide6.QtCore import Qt, Signal, QUrl
from PySide6.QtGui import QPixmap, QDesktopServices
from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout, QWidget, QHBoxLayout, QFileDialog
from qfluentwidgets import IconWidget, GroupHeaderCardWidget, PushButton, ComboBox, SearchLineEdit, PrimaryPushButton, \
    BodyLabel, InfoBarIcon,InfoBar,InfoBarPosition
from qfluentwidgets import FluentIcon as FIF
from app.common.style_sheet import StyleSheet


class SettinsCard(GroupHeaderCardWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("基本设置")
        self.setBorderRadius(8)
        self.out_chooseButton = PushButton("选择")
        self.comboBox = ComboBox()
        self.comboBox.addItems(["始终显示（首次打包时建议启用）", "始终隐藏"])
        self.main_chooseButton = PushButton("选择")

        self.hintIcon = IconWidget(InfoBarIcon.INFORMATION)
        self.hintLabel = BodyLabel("点击编译按钮以开始打包 👉")
        self.compileButton = PrimaryPushButton(FIF.PLAY_SOLID, "编译")
        self.openButton = PushButton(FIF.VIEW, "打开")

        self.__initWidget()
        self.connectSignalToSlot()

    def __initWidget(self):
        self.out_chooseButton.setFixedWidth(120)
        self.main_chooseButton.setFixedWidth(120)
        self.comboBox.setFixedWidth(320)
        self.hintIcon.setFixedSize(16, 16)

        # 设置底部工具栏布局
        self.bottomLayout = QHBoxLayout()

        self.bottomLayout.setSpacing(10)
        self.bottomLayout.setContentsMargins(24, 0, 24, 20)
        self.bottomLayout.addWidget(self.hintIcon, 0, Qt.AlignLeft)
        self.bottomLayout.addWidget(self.hintLabel, 0, Qt.AlignLeft)
        self.bottomLayout.addStretch(1)
        self.bottomLayout.addWidget(self.openButton, 0, Qt.AlignRight)
        self.bottomLayout.addWidget(self.compileButton, 0, Qt.AlignRight)
        self.bottomLayout.setAlignment(Qt.AlignVCenter)

        # 添加组件到分组中
        self.addGroup(FIF.ASTERISK, "构建目录", "选择 Nuitka 的输出目录", self.out_chooseButton)
        self.addGroup(FIF.ASTERISK, "运行终端", "设置是否显示命令行终端", self.comboBox)
        group = self.addGroup(FIF.ASTERISK, "入口脚本", "选择软件的入口脚本", self.main_chooseButton)
        group.setSeparatorVisible(True)


        # 添加底部工具栏
        self.vBoxLayout.addLayout(self.bottomLayout)

    def connectSignalToSlot(self):
        self.out_chooseButton.clicked.connect(self.outputDirChoose)
        self.main_chooseButton.clicked.connect(self.mainFunctionChoose)
        self.comboBox.currentIndexChanged.connect(self.onComboBoxChanged)
    def outputDirChoose(self):
        fileDir = QFileDialog.getExistingDirectory(self, "请选择Nuitka输出目录", "")
        print(fileDir)
        self.groupWidgets[0].setContent(fileDir)
        InfoBar.success(
            title='输出文件目录',
            content=f"{fileDir}",
            orient=Qt.Vertical,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )
    def mainFunctionChoose(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "请选择Python程序入口py文件", "",
                                                       "Python Files (*.py);;All Files (*)")
        print(fileName)
        self.groupWidgets[2].setContent(fileName)
        InfoBar.success(
            title='入口文件路径',
            content=f"{fileName}",
            orient=Qt.Vertical,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )

    def onComboBoxChanged(self, index):
        print(index)


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    from qfluentwidgets import setTheme, Theme
    from app.recource import resource_rc

    setTheme(Theme.LIGHT)
    app = QApplication(sys.argv)
    w = SettinsCard()
    w.show()
    app.exec()
