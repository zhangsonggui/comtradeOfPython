import sys

from PyQt6.QtWidgets import QApplication

from wave_main_impl import WaveMain

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wave_main = WaveMain()
    sys.exit(app.exec())
