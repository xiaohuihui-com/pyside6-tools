from PySide6.QtCore import Qt
from PySide6.QtWidgets import QVBoxLayout, QHBoxLayout, QWidget, QFileDialog

from qfluentwidgets import IconWidget, GroupHeaderCardWidget, PushButton, ComboBox, PrimaryPushButton, \
    BodyLabel, InfoBarIcon, InfoBar, InfoBarPosition
from qfluentwidgets import FluentIcon as FIF

from app.components.brief_card import BriefCardBase
from app.common.signal_bus import signalBus
import subprocess

class BriefCard(BriefCardBase):
    def __init__(self, icon, title, content, parent=None):
        super().__init__(icon, title, content, parent=parent)
        self.pyenv = None
        self.button = PushButton('Python解释器', self)
        self.hBoxLayout.addWidget(self.button, 0, Qt.AlignmentFlag.AlignRight)

        self.button.clicked.connect(self.pyenvChoose)

    def pyenvChoose(self):
        fileName, _ = QFileDialog.getOpenFileName(self, "请选择Python程序入口py文件", "D:\minianaconda\envs",
                                                  "Python Files (*.exe);;All Files (*)")
        self.pyenv = fileName
        print(fileName)
        InfoBar.success(
            title='Python解释器',
            content="虚拟环境Python解释器，加载成功！",
            orient=Qt.Horizontal,
            isClosable=True,
            position=InfoBarPosition.TOP_RIGHT,
            duration=2000,
            parent=self
        )


class SettinsCard(GroupHeaderCardWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle("基本设置")
        self.setBorderRadius(8)
        self.output = None
        self.main_function = None
        self.cmdable = 'enable'
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
        self.compileButton.clicked.connect(self.compile)

    def outputDirChoose(self):
        fileDir = QFileDialog.getExistingDirectory(self, "请选择Nuitka输出目录", "./")
        self.output = fileDir
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
        fileName, _ = QFileDialog.getOpenFileName(self, "请选择Python程序入口py文件", "./",
                                                  "Python Files (*.py);;All Files (*)")
        self.main_function = fileName
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
        if index == 0:
            self.cmdable = 'enable'
        else:
            self.cmdable = 'disable'
        print(index)

    def compile(self):
        signalBus.compileSignal.emit()


class NuitkaInterface(QWidget):
    """ Date time interface """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("NuitkaInterface")
        self.brife_card = BriefCard(
            icon=':/images/nuitka.png',
            title='Nuitka Tool',
            content=' Nuitka 是一个 Python 编译器。 Nuitka 的主要功能是将 Python 代码转换成 C 语言代码，再编译成机器代码，从而提高程序的运行效率。'
        )
        self.settings_card = SettinsCard()

        self.__initWidget()
        signalBus.compileSignal.connect(self.run_compile)

    def __initWidget(self):
        self.vbox = QVBoxLayout(self)
        self.vbox.setContentsMargins(6, 6, 6, 6)
        self.vbox.addWidget(self.brife_card)
        self.vbox.addWidget(self.settings_card, 0, Qt.AlignmentFlag.AlignTop)

    def run_compile(self):
        self.data = [self.brife_card.pyenv, self.settings_card.output, self.settings_card.main_function,
                     self.settings_card.cmdable]

        args = [
            f'{self.brife_card.pyenv} -m nuitka',
            '--standalone',
            f'--windows-console-mode={self.settings_card.cmdable}',
            '--enable-plugins=pyside6',
            '--nofollow-imports',
            f'--output-dir={self.settings_card.output}',
            '--show-progress',
            '--remove-output',
            f'{self.settings_card.main_function}'
        ]
        print(args)
        process = subprocess.Popen(" ".join(args),shell=True,
                                   universal_newlines=True,
                                   stdin=subprocess.PIPE,
                                   stderr=subprocess.STDOUT,
                                   stdout=subprocess.PIPE,
                                   errors='ignore')
        for line in process.stdout:
            print(line.strip())

        # 检查脚本的返回码
        if process.returncode != 0:
            print(f"脚本执行失败，返回码：{process.returncode}")
            # 可以选择打印stderr以获取更多错误信息
            print(process.stderr)


if __name__ == '__main__':
    import sys
    from PySide6.QtWidgets import QApplication
    from qfluentwidgets import setTheme, Theme
    from app.recource import resource_rc

    setTheme(Theme.LIGHT)
    app = QApplication(sys.argv)
    w = NuitkaInterface()
    w.show()
    app.exec()
