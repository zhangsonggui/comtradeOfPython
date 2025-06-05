from PyQt6.QtWidgets import (QMainWindow, QMessageBox)

from py3comtrade.reader.comtrade_reader import comtrade_reader
from select_channle_impl import SelectChannel
from wave_main import Ui_visualWave


class WaveMain(Ui_visualWave, QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()
        # self.showMaximized()
        self.comtrade = None
        self.do_open_file()
        self.actionopen.triggered.connect(self.do_open_file)
        self.select_channle.triggered.connect(self.open_select_channle_window)
        self.tabWidget.currentChanged.connect(self.on_tab_changed)

    def do_open_file(self):
        # filepath, filetype = QFileDialog.getOpenFileName(
        #     self, "打开文件", os.getcwd(), "comtrade files (*.cfg)")
        filepath = r"D:\codeArea\gitee\comtradeOfPython\tests\data\xtz.cfg"
        if filepath:
            self.setWindowTitle(f"{self.windowTitle()} - {filepath}")
            self.comtrade = comtrade_reader(filepath)

    def on_tab_changed(self, index):
        if self.comtrade is None:
            QMessageBox.warning(self, "警告", "请先打开录波文件")
            return
        if index == 0:
            pass
        elif index == 1:
            pass
        elif index == 2:
            pass
        elif index == 3:
            pass

    def open_select_channle_window(self):
        if self.comtrade is None:
            QMessageBox.warning(self, "警告", "请先打开录波文件")
            return
        self.sc = SelectChannel(self.comtrade.configure)
        self.sc.show()

    def on_analog_changed(self, text):
        self.textEdit.setPlainText(text)
