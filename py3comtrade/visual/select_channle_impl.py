from PyQt6 import QtWidgets
from PyQt6 import QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (QDialog)

from py3comtrade.model.analog import Analog
from py3comtrade.model.configure import Configure
from py3comtrade.model.digital import Digital
from select_channel import Ui_select_channle


class SelectChannel(Ui_select_channle, QDialog):
    def __init__(self, configure: Configure):
        super().__init__()
        self.setupUi(self)
        self.show()
        self.setWindowFlags(Qt.WindowType.Window | Qt.WindowType.WindowStaysOnTopHint)
        self.listWidget_analog.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.listWidget_digital.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ExtendedSelection)
        self.init_analog_list(configure.analogs)
        self.init_digital_list(configure.digitals)

    def init_analog_list(self, analogs: list[Analog]):
        for analog in analogs:
            self.listWidget_analog.addItem(analog.name)

    def init_digital_list(self, digitals: list[Digital]):
        for digital in digitals:
            self.listWidget_digital.addItem(digital.name)
