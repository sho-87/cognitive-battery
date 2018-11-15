import urllib

from designer import update_dialog_qt
from PyQt5 import QtCore, QtGui, QtWidgets
from utils import values
from xml.etree import ElementTree as etree


class UpdateDialog(QtWidgets.QDialog, update_dialog_qt.Ui_Dialog):
    def __init__(self, parent=None):
        super(UpdateDialog, self).__init__(parent)

        # Setup the update dialog box
        self.setupUi(self)

        # Set version number
        self.current_version = values.get_version()
        self.current_value.setText(self.current_version)

        # Define URLs
        self.links = values.get_links()

        # Delete the object when dialog is closed
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Remove the help / whats this button from title bar
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        # Bind button events
        self.btn_update.clicked.connect(self.show_releases)
        self.btn_close.clicked.connect(self.close)

        # Check for updates
        self.check_version()

    def check_version(self):
        try:
            url = urllib.request.urlopen(self.links["rss"])
            # convert to string:
            data = url.read()
            url.close()

            # entire feed
            root = etree.fromstring(data)

            releases = []
            for child in root.findall(".//{http://www.w3.org/2005/Atom}entry"):
                releases.append(child[0].text)

            latest_version = releases[0].split("/")[-1]
            self.latest_value.setText(latest_version)

            if self.current_version == latest_version:
                self.info.setText("No updates available.")
                self.current_value.setStyleSheet("color: green")
            else:
                self.btn_update.setEnabled(True)
                self.info.setText("New version available...")
                self.current_value.setStyleSheet("color: red")
        except urllib.error.URLError as e:
            self.info.setText(
                "Unable to retrieve version information. Check your internet connection..."
            )

    # Open web browser to the github releases page
    def show_releases(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.links["releases"]))
