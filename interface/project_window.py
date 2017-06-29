import os
import sys
import json

from PyQt5 import QtCore, QtGui, QtWidgets
from designer import project_window_qt
from interface import battery_window, project_new_window


class ProjectWindow(QtWidgets.QMainWindow, project_window_qt.Ui_ProjectWindow):
    def __init__(self, base_dir, first_run, res_width, res_height):
        super(ProjectWindow, self).__init__()

        # Setup the main window UI
        self.setupUi(self)

        # Set app icon
        self.setWindowIcon(QtGui.QIcon(os.path.join('images', 'icon_sml.png')))

        # Keep reference to main battery and new project windows
        self.main_battery = None
        self.new_project_window = None

        self.res_width = res_width
        self.res_height = res_height
        self.directory = base_dir
        self.first_run = first_run

        # Check if project list exists
        if not os.path.isfile(os.path.join(self.directory, 'projects.txt')):
            self.project_list = {}
            self.save_projects(self.project_list)
        else:
            self.project_list = self.refresh_projects()

        # Handle menu bar item click events
        self.actionNewProject.triggered.connect(self.new_project)
        self.actionExit.triggered.connect(self.close)

        # Bind button events
        self.startButton.clicked.connect(self.start)
        self.closeButton.clicked.connect(self.close)

    def new_project(self):
        self.new_project_window = project_new_window.NewProjectWindow(self.directory, self.project_list)
        self.new_project_window.show()

    def start(self, event):
        self.main_battery = battery_window.BatteryWindow(self.directory,
                                                         self.first_run,
                                                         self.res_width,
                                                         self.res_height)
        self.main_battery.show()
        self.close()

    def save_projects(self, projects):
        with open(os.path.join(self.directory, 'projects.txt'), 'w+') as f:
            json.dump(projects, f, indent=4)

    def refresh_projects(self):
        print "refresh"
        with open(os.path.join(self.directory, 'projects.txt'), 'r') as f:
            projects = json.load(f)

        return projects
