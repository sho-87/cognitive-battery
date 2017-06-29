import os
import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from designer import project_new_window_qt


class NewProjectWindow(QtWidgets.QDialog, project_new_window_qt.Ui_NewProjectWindow):
    def __init__(self):
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

        # Set input validators
        self.projectNameValue.setValidator(
            QtGui.QRegExpValidator(QtCore.QRegExp('[A-Za-z0-9 ]+')))

        # Bind button events
        self.dirSelectButton.clicked.connect(self.select_file)
        self.createButton.clicked.connect(self.close)
        self.cancelButton.clicked.connect(self.close)

    def select_file(self):
        self.file_dialog = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory for the project')
        self.dirValue.setText(self.file_dialog)
