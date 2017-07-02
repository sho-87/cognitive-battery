import os
import sys
import json
from datetime import datetime

from PyQt5 import QtGui, QtWidgets
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

        # Check if project file exists
        if not os.path.isfile(os.path.join(self.directory, 'projects.txt')):
            self.project_list = {}
            self.save_projects(self.project_list)
        else:
            self.project_list = self.refresh_projects()

        # Make info labels invisible at start
        self.researcherLabel.hide()
        self.createdLabel.hide()
        self.dirLabel.hide()

        # Handle menu bar item click events
        self.actionNewProject.triggered.connect(self.new_project)
        self.actionExit.triggered.connect(self.close)

        # Bind button events
        self.projectExpandButton.clicked.connect(self.projectTree.expandAll)
        self.projectCollapseButton.clicked.connect(self.projectTree.collapseAll)
        self.openButton.clicked.connect(self.start)

        # Project tree click event
        self.projectTree.itemClicked.connect(self.project_click)

    def new_project(self):
        self.new_project_window = project_new_window.NewProjectWindow(self.directory, self.project_list)
        self.new_project_window.exec_()
        self.refresh_projects()

    def project_click(self, item):
        if item.parent():
            researcher = item.parent().text(0)
            project_name = item.text(0)

            created_unix = self.project_list[researcher][project_name]["created"]
            created_time = datetime.fromtimestamp(created_unix).strftime("%d/%m/%Y @ %H:%M")
            project_path = self.project_list[researcher][project_name]["path"]

            self.projectName.setText(project_name)
            self.researcherValue.setText(researcher)
            self.createdValue.setText(created_time)
            self.dirValue.setText(project_path)

            # Enable buttons and labels
            self.researcherLabel.show()
            self.createdLabel.show()
            self.dirLabel.show()
            self.openButton.setEnabled(True)
            self.deleteButton.setEnabled(True)

    def start(self, event):
        self.main_battery = battery_window.BatteryWindow(self.directory,
                                                         self.first_run,
                                                         self.res_width,
                                                         self.res_height)
        self.main_battery.show()
        self.close()

    def save_projects(self, projects):
        # Save current project list to file
        with open(os.path.join(self.directory, 'projects.txt'), 'w+') as f:
            json.dump(projects, f, indent=4)

    def refresh_projects(self):
        # Load most recent saved project list from file
        with open(os.path.join(self.directory, 'projects.txt'), 'r') as f:
            projects = json.load(f)

        # Clear existing tree widget
        self.projectTree.clear()

        # Get all researcher names
        for person in projects.keys():
            # Add researcher root node
            personItem = QtWidgets.QTreeWidgetItem([person])
            font = personItem.font(0)
            font.setBold(True)
            personItem.setFont(0, font)
            self.projectTree.addTopLevelItem(personItem)

            # Add project name for each researcher
            for project in projects[person].keys():
                projectItem = QtWidgets.QTreeWidgetItem([project])
                personItem.addChild(projectItem)

        self.projectTree.expandAll()

        return projects
