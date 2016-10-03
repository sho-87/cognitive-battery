import os
import sys
import random
import datetime
import pygame
import pandas as pd
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui

from utils import display
from designer import battery_window_qt
from interface import about_dialog, settings_window
from tasks import ant, mrt, sart, ravens, digitspan_backwards, sternberg


class BatteryWindow(QtGui.QMainWindow, battery_window_qt.Ui_CognitiveBattery):
    def __init__(self, cur_directory, first_run, res_width, res_height):
        super(BatteryWindow, self).__init__()

        # Setup the main window UI
        self.setupUi(self)

        # Set app icon
        self.setWindowIcon(QtGui.QIcon(os.path.join('images', 'icon.png')))

        # Get screen resolution
        self.res_width = res_width
        self.res_height = res_height

        # Create/open settings file with no registry fallback
        self.settings = QtCore.QSettings("settings.ini",
                                         QtCore.QSettings.IniFormat)
        self.settings.setFallbacksEnabled(False)

        # If first run, store some default settings
        if first_run:
            # Main window size and position
            self.save_settings_window(self.size(), QtCore.QPoint(100, 100))

            # Settings - Task Windows
            self.settings.beginGroup("TaskWindows")
            self.settings.setValue('fullscreen', False)
            self.settings.setValue('borderless', False)
            self.settings.setValue('width', 1280)
            self.settings.setValue('height', 1024)
            self.settings.endGroup()

        # Set initial window size/pos from saved settings
        self.settings.beginGroup("MainWindow")
        self.resize(self.settings.value("size").toSize())
        self.move(self.settings.value("pos").toPoint())
        self.settings.endGroup()

        # Initialize task settings
        self.task_fullscreen = None
        self.task_borderless = None
        self.task_width = None
        self.task_height = None

        # Initialize the about and settings window objects
        self.about = None
        self.settings_window = None

        # Initialize pygame screen
        self.pygame_screen = None

        # Define URLs
        self.LINKS = {
            "github": "https://github.com/sho-87/cognitive-battery",
            "license": "https://github.com/sho-87/"
                       "cognitive-battery/blob/master/LICENSE",
            "develop": "https://github.com/sho-87/"
                       "cognitive-battery/tree/develop",
            "issues": "https://github.com/sho-87/cognitive-battery/issues",
            "new_issue": "https://github.com/sho-87/"
                         "cognitive-battery/issues/new"
        }

        # Get current directory
        self.directory = cur_directory

        # Make data folder if it doesnt exist
        self.dataPath = os.path.join(self.directory, "data")
        if not os.path.isdir(self.dataPath):
            os.makedirs(self.dataPath)

        # Get list of existing experiment names/IDs currently in use
        self.tempNames = []
        for fileName in os.listdir(self.dataPath):
            if fileName.endswith(".xls"):
                self.tempNames.append(fileName.split("_")[0])

        self.expNames = list(set(self.tempNames))

        # Autocomplete for experiment name/ID
        self.experiments = QtCore.QString(';'.join(self.expNames)).split(";")
        self.completer = QtGui.QCompleter(self.experiments,
                                          self.experimentIDBox)
        self.experimentIDBox.setCompleter(self.completer)

        # Handle menu bar item click events
        self.actionExit.triggered.connect(self.close)
        self.actionSettings.triggered.connect(self.show_settings)
        self.actionDocumentation.triggered.connect(self.show_documentation)
        self.actionLicense.triggered.connect(self.show_license)
        self.actionContribute.triggered.connect(self.show_contribute)
        self.actionBrowse_Issues.triggered.connect(self.show_browse_issues)
        self.actionReport_Bug.triggered.connect(self.show_new_issue)
        self.actionRequest_Feature.triggered.connect(self.show_new_issue)
        self.actionAbout.triggered.connect(self.show_about)

        # Bind button events
        self.cancelButton.clicked.connect(self.close)
        self.startButton.clicked.connect(self.start)
        self.randomOrderCheck.clicked.connect(self.random_order_selected)
        self.selectAllButton.clicked.connect(self.select_all)
        self.deselectAllButton.clicked.connect(self.deselect_all)
        self.upButton.clicked.connect(self.move_up)
        self.downButton.clicked.connect(self.move_down)

    # Open web browser to the documentation page
    def show_documentation(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.LINKS["github"]))

    # Open web browser to the license page
    def show_license(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.LINKS["license"]))

    # Open web browser to the github develop branch for contribution
    def show_contribute(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.LINKS["develop"]))

    # Open web browser to the github issues page
    def show_browse_issues(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.LINKS["issues"]))

    # Open web browser to the github new issue post
    def show_new_issue(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.LINKS["new_issue"]))

    # Create a new SettingsWindow object and display it
    def show_settings(self):
        # If the settings window does not exist, create one
        if self.settings_window is None:
            self.settings_window = settings_window.SettingsWindow(self)
            self.settings_window.show()
            self.settings_window.finished.connect(
                lambda: setattr(self, 'settings_window', None))
        # If settings window exists, bring it to the front
        else:
            self.settings_window.activateWindow()
            self.settings_window.raise_()

    # Create a new AboutDialog object and display it
    def show_about(self):
        # If the about dialog does not exist, create one
        if self.about is None:
            self.about = about_dialog.AboutDialog(self)
            self.about.show()
            self.about.finished.connect(lambda: setattr(self, 'about', None))
        # If about dialog exists, bring it to the front
        else:
            self.about.activateWindow()
            self.about.raise_()

    def error_dialog(self, message):
        QtGui.QMessageBox.warning(self, 'Error', message)

    def random_order_selected(self):
        if self.randomOrderCheck.isChecked():
            self.upButton.setEnabled(False)
            self.downButton.setEnabled(False)
            return True
        else:
            self.upButton.setEnabled(True)
            self.downButton.setEnabled(True)
            return False

    def select_all(self):
        for index in range(self.taskList.count()):
            self.taskList.item(index).setCheckState(2)

    def deselect_all(self):
        for index in range(self.taskList.count()):
            self.taskList.item(index).setCheckState(0)

    def move_up(self):
        current_row = self.taskList.currentRow()
        current_item = self.taskList.takeItem(current_row)
        self.taskList.insertItem(current_row - 1, current_item)
        self.taskList.setCurrentItem(current_item)

    def move_down(self):
        current_row = self.taskList.currentRow()
        current_item = self.taskList.takeItem(current_row)
        self.taskList.insertItem(current_row + 1, current_item)
        self.taskList.setCurrentItem(current_item)

    # Save window size/position to settings file
    def save_settings_window(self, size, pos):
        self.settings.beginGroup("MainWindow")
        self.settings.setValue('size', size)
        self.settings.setValue('pos', pos)
        self.settings.endGroup()

    # Get task window settings from file
    def get_task_settings(self):
        self.settings.beginGroup("TaskWindows")
        self.task_fullscreen = self.settings.value("fullscreen").toBool()
        self.task_borderless = self.settings.value("borderless").toBool()
        self.task_width = self.settings.value("width").toInt()[0]
        self.task_height = self.settings.value("height").toInt()[0]
        self.settings.endGroup()

    # Override the closeEvent method
    def closeEvent(self, event):
        self.save_settings_window(self.size(), self.pos())

        event.accept()
        sys.exit(0)  # This closes any open pygame windows

    def start(self):
        # Store input values
        sub_num = self.subNumBox.text()
        experiment_id = self.experimentIDBox.text()
        condition = self.conditionBox.text()
        age = self.ageBox.text()
        ra = self.raBox.text()
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        if self.maleRadio.isChecked():
            sex = 'male'
        else:
            sex = 'female'

        # Get *selected* tasks and task order
        selected_tasks = []
        for index in range(self.taskList.count()):
            # State 2 is set when item is selected
            if self.taskList.item(index).checkState() == 2:
                # Add selected task to task list
                selected_tasks.append(str(self.taskList.item(index).text()))

        # Check to see if a random order is desired
        # If so, shuffle tasks
        if self.random_order_selected():
            random.shuffle(selected_tasks)

        # Check for required inputs
        if not selected_tasks:
            self.error_dialog('No tasks selected')
        elif not ra:
            self.error_dialog('Please enter RA name...')
        elif not sub_num:
            self.error_dialog('Please enter a subject number...')
        elif not experiment_id:
            self.error_dialog('Please enter an experiment ID...')
        elif not condition:
            self.error_dialog('Please enter a condition number...')
        elif not age:
            self.error_dialog('Please enter an age...')
        elif not self.maleRadio.isChecked() and not \
                self.femaleRadio.isChecked():
            self.error_dialog('Please select a sex...')
        else:
            # Store subject info into a dataframe
            subject_info = pd.DataFrame(
                data=[(str(current_date), str(sub_num), str(experiment_id),
                       str(condition), int(age), str(sex), str(ra),
                       ', '.join(selected_tasks))],
                columns=['datetime', 'sub_num', 'expID', 'condition',
                         'age', 'sex', 'RA', 'tasks']
            )

            # Set the output file name
            data_file_name = "%s_%s_%s.xls" % (experiment_id, sub_num,
                                               condition)

            # Check if file already exists
            output_file = os.path.join(self.dataPath, data_file_name)
            if os.path.isfile(output_file):
                self.error_dialog('Data file already exists')
            else:
                # Create the excel writer object and save the file
                writer = pd.ExcelWriter(output_file)
                subject_info.to_excel(writer, 'info', index=False)
                writer.save()

                # Minimize battery UI
                self.showMinimized()

                # Get most recent task window settings from file
                self.get_task_settings()

                # Center all pygame windows if not fullscreen
                if not self.task_fullscreen:
                    pos_x = str(self.res_width / 2 - self.task_width / 2)
                    pos_y = str(self.res_height / 2 - self.task_height / 2)

                    os.environ['SDL_VIDEO_WINDOW_POS'] = \
                        "%s, %s" % (pos_x, pos_y)

                # Initialize pygame
                pygame.init()

                # Create primary task window
                # pygame_screen is passed to each task as the display window
                if self.task_fullscreen:
                    self.pygame_screen = pygame.display.set_mode(
                        (0, 0), pygame.FULLSCREEN)
                else:
                    if self.task_borderless:
                        self.pygame_screen = pygame.display.set_mode(
                            (self.task_width, self.task_height),
                            pygame.NOFRAME)
                    else:
                        self.pygame_screen = pygame.display.set_mode(
                            (self.task_width, self.task_height))

                background = pygame.Surface(self.pygame_screen.get_size())
                background = background.convert()

                # Run each task
                # Return and save their output to dataframe/excel
                for task in selected_tasks:
                    if task == "Attention Network Test (ANT)":
                        # Set number of blocks for ANT
                        ant_task = ant.ANT(self.pygame_screen, background,
                                           blocks=2)
                        # Run ANT
                        ant_data = ant_task.run()
                        # Save ANT data to excel
                        ant_data.to_excel(writer, 'ANT', index=False)
                    elif task == "Mental Rotation Task":
                        mrt_task = mrt.MRT(self.pygame_screen, background)
                        # Run MRT
                        mrt_data = mrt_task.run()
                        # Save MRT data to excel
                        mrt_data.to_excel(writer, 'MRT', index=False)
                    elif task == "Sustained Attention to Response Task (SART)":
                        sart_task = sart.SART(self.pygame_screen, background)
                        # Run SART
                        sart_data = sart_task.run()
                        # Save SART data to excel
                        sart_data.to_excel(writer, 'SART', index=False)
                    elif task == "Digit Span (backwards)":
                        digitspan_backwards_task = \
                            digitspan_backwards.DigitspanBackwards(
                                self.pygame_screen, background)
                        # Run Digit span (Backwards)
                        digitspan_backwards_data = \
                            digitspan_backwards_task.run()
                        # Save digit span (backwards) data to excel
                        digitspan_backwards_data.to_excel(
                            writer, 'Digit span (backwards)', index=False)
                    elif task == "Raven's Progressive Matrices":
                        ravens_task = ravens.Ravens(
                            self.pygame_screen, background,
                            start=9, numTrials=12)
                        # Run Raven's Matrices
                        ravens_data = ravens_task.run()
                        # Save ravens data to excel
                        ravens_data.to_excel(writer, 'Ravens Matrices',
                                             index=False)
                    elif task == "Sternberg Task":
                        sternberg_task = sternberg.Sternberg(
                            self.pygame_screen, background)
                        # Run Sternberg Task
                        sternberg_data = sternberg_task.run()
                        # Save sternberg data to excel
                        sternberg_data.to_excel(writer, 'Sternberg',
                                                index=False)

                    # Save excel file
                    writer.save()

                # End of experiment screen
                pygame.display.set_caption("Cognitive Battery")
                pygame.mouse.set_visible(1)

                background.fill((255, 255, 255))
                self.pygame_screen.blit(background, (0, 0))

                font = pygame.font.SysFont("arial", 30)
                display.text(self.pygame_screen, font, "End of Experiment",
                             "center", "center")

                pygame.display.flip()

                display.wait_for_space()

                # Quit pygame
                pygame.quit()

                print "--- Experiment complete"
                self.close()


def main():
    # Get current directory
    cur_directory = os.path.dirname(os.path.realpath(__file__))

    # Check if settings file exists. If not, this is a first run
    first_run = not os.path.isfile(os.path.join(cur_directory, "settings.ini"))

    # Create main app window
    app = QtGui.QApplication(sys.argv)
    screen_resolution = app.desktop().screenGeometry()

    battery_window = BatteryWindow(cur_directory,
                                   first_run,
                                   screen_resolution.width(),
                                   screen_resolution.height())
    battery_window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
