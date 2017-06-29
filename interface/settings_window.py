from PyQt5 import QtCore, QtGui, QtWidgets
from designer import settings_window_qt


class SettingsWindow(QtWidgets.QDialog, settings_window_qt.Ui_SettingsDialog):
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

        # Set initial settings window size from saved settings
        self.settings.beginGroup("SettingsWindow")
        self.resize(self.settings.value("size", self.size()))
        self.settings.endGroup()

        # Get stored task window settings
        self.settings.beginGroup("TaskWindows")

        if self.settings.value("fullscreen") == "true":
            self.task_fullscreen = True
        else:
            self.task_fullscreen = False

        if self.settings.value("borderless") == "true":
            self.task_borderless = True
        else:
            self.task_borderless = False

        self.task_width = str(self.settings.value("width"))
        self.task_height = str(self.settings.value("height"))
        self.settings.endGroup()

        # Set task window values
        self.settings_task_height_value.setText(self.task_height)
        self.settings_task_width_value.setText(self.task_width)

        # Set fullscreen check state
        self.settings_task_fullscreen_checkbox.setChecked(self.task_fullscreen)

        # Set borderless check state
        self.settings_task_borderless_checkbox.setChecked(self.task_borderless)

        # Set state of the windowed mode options (e.g. borderless, size)
        self.set_windowed_options_state(not self.task_fullscreen)

        # Bind button events
        self.settings_save_button.clicked.connect(self.save_settings)
        self.settings_cancel_button.clicked.connect(self.cancel_settings)
        self.settings_task_fullscreen_checkbox.clicked.connect(
            self.task_fullscreen_checkbox)

    def set_windowed_options_state(self, state):
        self.settings_task_borderless_checkbox.setEnabled(state)

        self.settings_task_height_value.setEnabled(state)
        self.settings_task_width_value.setEnabled(state)

    def task_fullscreen_checkbox(self):
        # Invert fullscreen selection state
        self.task_fullscreen = not self.task_fullscreen
        # Set entry boxes to opposite of new fullscreen state
        self.set_windowed_options_state(not self.task_fullscreen)

    def save_window_information(self):
        self.settings.beginGroup("SettingsWindow")
        self.settings.setValue('size', self.size())
        self.settings.endGroup()

    def save_settings(self):
        self.settings.beginGroup("TaskWindows")
        self.settings.setValue('fullscreen', self.task_fullscreen)

        # Only save some options if fullscreen is not selected
        if not self.task_fullscreen:
            self.settings.setValue(
                'borderless',
                self.settings_task_borderless_checkbox.isChecked())

            self.settings.setValue('width',
                                   self.settings_task_width_value.text())
            self.settings.setValue('height',
                                   self.settings_task_height_value.text())

        self.settings.endGroup()

        # Save settings window size information
        self.save_window_information()
        self.close()

    def cancel_settings(self):
        # Save settings window size information
        self.save_window_information()
        self.close()
