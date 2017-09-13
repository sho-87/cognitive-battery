from PyQt5 import QtCore, QtGui, QtWidgets
from designer import settings_window_qt


class SettingsWindow(QtWidgets.QDialog, settings_window_qt.Ui_SettingsDialog):
    def __init__(self, parent, settings):
        super(SettingsWindow, self).__init__(parent)

        # Setup the about dialog box
        self.setupUi(self)

        # Delete the object when dialog is closed
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        # Remove the help / whats this button from title bar
        self.setWindowFlags(
            self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        # Open settings file with no registry fallback
        self.settings = settings

        # Set initial settings window size from saved settings
        self.settings.beginGroup("SettingsWindow")
        self.resize(self.settings.value("size", self.size()))
        self.settings.endGroup()

        # General settings
        self.settings.beginGroup("GeneralSettings")

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

        if self.settings.value("taskBeep") == "true":
            self.task_beep = True
        else:
            self.task_beep = False

        self.settings.endGroup()

        # Set task window values
        self.settings_task_height_value.setText(self.task_height)
        self.settings_task_width_value.setText(self.task_width)

        # Set fullscreen check state
        self.settings_task_fullscreen_checkbox.setChecked(self.task_fullscreen)

        # Set borderless check state
        self.settings_task_borderless_checkbox.setChecked(self.task_borderless)

        # Set task beep check state
        self.settings_task_beep_checkbox.setChecked(self.task_beep)

        # Set state of the windowed mode options (e.g. borderless, size)
        self.set_windowed_options_state(not self.task_fullscreen)

        # ANT settings
        self.settings.beginGroup("AttentionNetworkTest")
        self.ant_blocks = str(self.settings.value("numBlocks"))
        self.settings_ant_blocks_value.setText(self.ant_blocks)
        self.settings.endGroup()

        # Flanker settings
        self.settings.beginGroup("Flanker")
        if self.settings.value("darkMode") == "true":
            self.flanker_dark = True
        else:
            self.flanker_dark = False

        self.settings_flanker_dark.setChecked(self.flanker_dark)

        self.flanker_compatible_blocks = str(self.settings.value("blocksCompat"))
        self.settings_flanker_compat_value.setText(self.flanker_compatible_blocks)

        self.flanker_incompatible_blocks = str(self.settings.value("blocksIncompat"))
        self.settings_flanker_incompat_value.setText(self.flanker_incompatible_blocks)

        self.flanker_order = str(self.settings.value("blockOrder"))

        if self.flanker_order == "compatible":
            self.settings_flanker_order_compat.setChecked(True)
        elif self.flanker_order == "incompatible":
            self.settings_flanker_order_incompat.setChecked(True)
        elif self.flanker_order == "choose":
            self.settings_flanker_order_choose.setChecked(True)

        self.settings.endGroup()

        # Ravens settings
        self.settings.beginGroup("Ravens")
        self.ravens_start = str(self.settings.value("startImage"))
        self.settings_ravens_start_value.setText(self.ravens_start)

        self.ravens_trials = str(self.settings.value("numTrials"))
        self.settings_ravens_trials_value.setText(self.ravens_trials)
        self.settings.endGroup()

        # Sternberg settings
        self.settings.beginGroup("Sternberg")
        self.sternberg_blocks = str(self.settings.value("numBlocks"))
        self.settings_sternberg_blocks_value.setText(self.sternberg_blocks)
        self.settings.endGroup()

        # Set input validators
        self.regex_numbers = QtGui.QRegExpValidator(QtCore.QRegExp('[0-9]+'))
        self.settings_ant_blocks_value.setValidator(self.regex_numbers)
        self.settings_flanker_compat_value.setValidator(self.regex_numbers)
        self.settings_flanker_incompat_value.setValidator(self.regex_numbers)
        self.settings_ravens_start_value.setValidator(self.regex_numbers)
        self.settings_ravens_trials_value.setValidator(self.regex_numbers)
        self.settings_sternberg_blocks_value.setValidator(self.regex_numbers)

        # Set starting toolbox item
        self.settings_toolbox.setCurrentIndex(0)

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
        # Check if Ravens images are in range (cant exceed 36 total)
        if int(self.settings_ravens_start_value.text()) > (36 - int(self.settings_ravens_trials_value.text()) + 1):
            QtWidgets.QMessageBox.warning(self, 'Ravens Progressive Matrices Error',
                                                'Too many images for Ravens task. '
                                                'Start with an earlier image, or use fewer trials')
        else:
            # General settings
            self.settings.beginGroup("GeneralSettings")
            self.settings.setValue('fullscreen',
                                   str(self.settings_task_fullscreen_checkbox.isChecked()).lower())

            # Only save some options if fullscreen is not selected
            if not self.task_fullscreen:
                self.settings.setValue(
                    'borderless',
                    str(self.settings_task_borderless_checkbox.isChecked()).lower())

                self.settings.setValue('width',
                                       self.settings_task_width_value.text())
                self.settings.setValue('height',
                                       self.settings_task_height_value.text())

            # Task beep setting
            self.settings.setValue('taskBeep', 
                                   str(self.settings_task_beep_checkbox.isChecked()).lower())
            self.settings.endGroup()

            # ANT settings
            self.settings.beginGroup("AttentionNetworkTest")
            self.settings.setValue("numBlocks", self.settings_ant_blocks_value.text())
            self.settings.endGroup()

            # Flanker settings
            self.settings.beginGroup("Flanker")
            self.settings.setValue("darkMode", str(self.settings_flanker_dark.isChecked()).lower())
            self.settings.setValue("blocksCompat", self.settings_flanker_compat_value.text())
            self.settings.setValue("blocksIncompat", self.settings_flanker_incompat_value.text())

            if self.settings_flanker_order_compat.isChecked():
                self.settings.setValue("blockOrder", "compatible")
            elif self.settings_flanker_order_incompat.isChecked():
                self.settings.setValue("blockOrder", "incompatible")
            elif self.settings_flanker_order_choose.isChecked():
                self.settings.setValue("blockOrder", "choose")

            self.settings.endGroup()

            # Ravens settings
            self.settings.beginGroup("Ravens")
            self.settings.setValue("startImage", self.settings_ravens_start_value.text())
            self.settings.setValue("numTrials", self.settings_ravens_trials_value.text())
            self.settings.endGroup()

            # Sternberg settings
            self.settings.beginGroup("Sternberg")
            self.settings.setValue("numBlocks", self.settings_sternberg_blocks_value.text())
            self.settings.endGroup()

            # Save settings window size information
            self.save_window_information()
            self.close()

    def cancel_settings(self):
        # Save settings window size information
        self.save_window_information()
        self.close()
