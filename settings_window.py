import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui

from interface import settings_window_qt


class SettingsWindow(QtGui.QDialog, settings_window_qt.Ui_SettingsDialog):
    def __init__(self, parent=None):
        super(SettingsWindow, self).__init__(parent)

        # Setup the about dialog box
        self.setupUi(self)

        # Delete the object when dialog is closed
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Remove the help / whats this button from title bar
        self.setWindowFlags(
            self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)
