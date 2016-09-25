import sys
import os
import random
import datetime
import pandas as pd
import ant
import mrt
import sart
import ravens
import digitspan_backwards
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui

from interface import main_window


class BatteryWindow(QtGui.QMainWindow, main_window.Ui_CognitiveBattery):
    def __init__(self):
        super(BatteryWindow, self).__init__()

        # Setup the main window ui
        self.setupUi(self)


def main():
    # Create main app window
    app = QtGui.QApplication(sys.argv)
    battery_window = BatteryWindow()
    battery_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
