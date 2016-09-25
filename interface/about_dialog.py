import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui

from designer import about_dialog_qt


class AboutDialog(QtGui.QDialog, about_dialog_qt.Ui_Dialog):
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)

        # Setup the about dialog box
        self.setupUi(self)

        # Delete the object when dialog is closed
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Remove the help / whats this button from title bar
        self.setWindowFlags(
            self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)