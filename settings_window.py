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

        # Open settings file with no registry fallback
        self.settings = QtCore.QSettings("settings.ini",
                                         QtCore.QSettings.IniFormat)
        self.settings.setFallbacksEnabled(False)

        # Get task window settings
        self.settings.beginGroup("TaskWindows")
        self.task_fullscreen = self.settings.value("fullscreen").toBool()
        self.task_width = self.settings.value("width").toString()
        self.task_height = self.settings.value("height").toString()
        self.settings.endGroup()

        # Set task window values
        self.settings_task_height_value.setText(self.task_height)
        self.settings_task_width_value.setText(self.task_width)

        # Set fullscreen check state
        self.settings_task_fullscreen_checkbox.setChecked(self.task_fullscreen)

        # Disable task window size entry if fullscreen is selected
        self.set_task_size_state(not self.task_fullscreen)

        # Bind button events
        self.settings_save_button.clicked.connect(self.save_settings)
        self.settings_cancel_button.clicked.connect(self.close)
        self.settings_task_fullscreen_checkbox.clicked.connect(
            self.task_fullscreen_checkbox)

    # Set state of the task window size entry fields
    def set_task_size_state(self, state):
        self.settings_task_height_value.setEnabled(state)
        self.settings_task_width_value.setEnabled(state)

    def task_fullscreen_checkbox(self):
        # Invert fullscreen selection state
        self.task_fullscreen = not self.task_fullscreen
        # Set entry boxes to opposite of new fullscreen state
        self.set_task_size_state(not self.task_fullscreen)

    def save_settings(self):
        self.settings.beginGroup("TaskWindows")
        self.settings.setValue('fullscreen', self.task_fullscreen)

        # Only save width and height if fullscreen is not selected
        if not self.task_fullscreen:
            self.settings.setValue('width',
                                   self.settings_task_width_value.text())
            self.settings.setValue('height',
                                   self.settings_task_height_value.text())

        self.settings.endGroup()

        self.close()
