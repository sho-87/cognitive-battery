import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from designer import project_window_qt
from interface import battery_window


class ProjectWindow(QtWidgets.QMainWindow, project_window_qt.Ui_ProjectWindow):
    def __init__(self, cur_directory, first_run, res_width, res_height):
        super(ProjectWindow, self).__init__()

        # Setup the main window UI
        self.setupUi(self)

        # Set app icon
        self.setWindowIcon(QtGui.QIcon(os.path.join('images', 'icon_sml.png')))

        # Keep reference to main battery window
        self.main_battery = None

        self.res_width = res_width
        self.res_height = res_height
        self.directory = cur_directory
        self.first_run = first_run

        # Handle menu bar item click events
        self.actionExit.triggered.connect(self.close)

        # Bind button events
        self.startButton.clicked.connect(self.start)
        self.closeButton.clicked.connect(self.close)

    def start(self, event):
        self.main_battery = battery_window.BatteryWindow(self.directory,
                                                   self.first_run,
                                                   self.res_width,
                                                   self.res_height)
        self.main_battery.show()
        self.close()
