import os
import sys
import json
import time

from PyQt5 import QtCore, QtGui, QtWidgets
from designer import project_new_window_qt


class NewProjectWindow(QtWidgets.QDialog, project_new_window_qt.Ui_NewProjectWindow):
    def __init__(self, base_dir, project_list):
        super(NewProjectWindow, self).__init__()

        # Setup the main window UI
        self.setupUi(self)

        # Set app icon
        self.setWindowIcon(QtGui.QIcon(os.path.join('images', 'icon_sml.png')))

        # Delete the object when dialog is closed
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Remove the help / whats this button from title bar
        self.setWindowFlags(
            self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.project_list = project_list
        self.base_dir = base_dir

        # Set input validators
        self.projectNameValue.setValidator(
            QtGui.QRegExpValidator(QtCore.QRegExp('[A-Za-z0-9 ]+')))

        # Bind button events
        self.dirSelectButton.clicked.connect(self.select_file)
        self.createButton.clicked.connect(self.create_project)
        self.cancelButton.clicked.connect(self.close)

    def select_file(self):
        self.file_dialog = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory for the project')
        self.dirValue.setText(self.file_dialog)

    def create_project(self):
        project_name = self.projectNameValue.text()
        researcher = self.researcherValue.text()
        dir_path = self.dirValue.text()

        if project_name != "" and researcher != "" and dir_path != "":
            if project_name not in list(self.project_list.keys()):
                self.project_list[project_name] = {'created': time.time(),
                                                   'researcher': researcher,
                                                   'path': dir_path}

                with open(os.path.join(self.base_dir, 'projects.txt'), 'w+') as f:
                    json.dump(self.project_list, f, indent=4)

                self.close()
            else:
               QtWidgets.QMessageBox.warning(self, 'Error', 'Project name already exists') 
        else:
            QtWidgets.QMessageBox.warning(self, 'Error', 'Please complete every field')
