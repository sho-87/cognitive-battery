import sys
import os
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
    # TODO move this class to a separate file
    def __init__(self, cur_directory, first_run, res_width, res_height):
        super(BatteryWindow, self).__init__()

        # Setup the main window UI
        self.setupUi(self)

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
        self.task_width = None
        self.task_height = None

        # Initialize the about and settings window objects
        self.about = None
        self.settings_window = None

        # Initialize pygame screen
        self.pygame_screen = None

        # Get current directory
        self.directory = cur_directory

        # Make data folder if it doesnt exist
        self.dataPath = self.directory + "\data\\"
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
        QtGui.QDesktopServices.openUrl(
            QtCore.QUrl("https://github.com/sho-87/cognitive-battery"))

    # Open web browser to the license page
    def show_license(self):
        QtGui.QDesktopServices.openUrl(
            QtCore.QUrl(
                "https://github.com/sho-87/cognitive-battery/blob/master/LICENSE"))

    # Open web browser to the github develop branch for contribution
    def show_contribute(self):
        QtGui.QDesktopServices.openUrl(
            QtCore.QUrl(
                "https://github.com/sho-87/cognitive-battery/tree/develop"))

    # Open web browser to the github issues page
    def show_browse_issues(self):
        QtGui.QDesktopServices.openUrl(
            QtCore.QUrl("https://github.com/sho-87/cognitive-battery/issues"))

    # Open web browser to the github new issue post
    def show_new_issue(self):
        QtGui.QDesktopServices.openUrl(
            QtCore.QUrl(
                "https://github.com/sho-87/cognitive-battery/issues/new"))

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
        currentRow = self.taskList.currentRow()
        currentItem = self.taskList.takeItem(currentRow)
        self.taskList.insertItem(currentRow - 1, currentItem)
        self.taskList.setCurrentItem(currentItem)

    def move_down(self):
        currentRow = self.taskList.currentRow()
        currentItem = self.taskList.takeItem(currentRow)
        self.taskList.insertItem(currentRow + 1, currentItem)
        self.taskList.setCurrentItem(currentItem)

    # TODO add memory for previously selected tasks
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
        self.task_width = self.settings.value("width").toInt()[0]
        self.task_height = self.settings.value("height").toInt()[0]

    # Redefine the closeEvent method
    def closeEvent(self, event):
        self.save_settings_window(self.size(), self.pos())

        event.accept()

        sys.exit(0)  # This closes any open pygame windows

    def start(self):
        # Store input values
        self.subNum = self.subNumBox.text()
        self.experimentID = self.experimentIDBox.text()
        self.condition = self.conditionBox.text()
        self.age = self.ageBox.text()
        self.ra = self.raBox.text()
        self.datetime = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        if self.maleRadio.isChecked():
            self.sex = 'male'
        elif self.femaleRadio.isChecked():
            self.sex = 'female'

        # Get *selected* tasks and task order
        self.tasks = []
        for index in range(self.taskList.count()):
            # State 2 is set when item is selected
            if self.taskList.item(index).checkState() == 2:
                # Add selected task to task list
                self.tasks.append(str(self.taskList.item(index).text()))

        # Check to see if a random order is desired
        # If so, shuffle tasks
        if self.random_order_selected():
            random.shuffle(self.tasks)

        # Check for required inputs
        if not self.tasks:
            self.error_dialog('No tasks selected')
        elif not self.ra:
            self.error_dialog('Please enter RA name...')
        elif not self.subNum:
            self.error_dialog('Please enter a subject number...')
        elif not self.experimentID:
            self.error_dialog('Please enter an experiment ID...')
        elif not self.condition:
            self.error_dialog('Please enter a condition number...')
        elif not self.age:
            self.error_dialog('Please enter an age...')
        elif not self.maleRadio.isChecked() and not self.femaleRadio.isChecked():
            self.error_dialog('Please select a sex...')
        else:
            # Store subject info into a dataframe
            self.subjectInfo = pd.DataFrame(
                data=[(str(self.datetime), str(self.subNum),
                       str(self.experimentID), str(self.condition),
                       int(self.age), str(self.sex), str(self.ra),
                       ', '.join(self.tasks))],
                columns=['datetime', 'subNum', 'expID', 'condition',
                         'age', 'sex', 'RA', 'tasks']
            )

            # Set the output file name
            self.datafileName = "%s_%s_%s.xls" % (self.experimentID,
                                                  self.subNum, self.condition)

            # Check if file already exists
            # TODO use OS path join to create paths
            if os.path.isfile(self.dataPath + self.datafileName):
                self.error_dialog('Data file already exists!')
            else:
                # TODO save each experiment data to their own directory
                # Create the excel writer object and save the file
                self.writer = pd.ExcelWriter(self.dataPath + self.datafileName)
                self.subjectInfo.to_excel(self.writer, 'info', index=False)
                self.writer.save()

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
                    self.pygame_screen = pygame.display.set_mode(
                        (self.task_width, self.task_height))

                # Run each task
                # Return and save their output to dataframe/excel
                # TODO move data saving to end of each individual task module
                for task in self.tasks:
                    if task == "Attention Network Test (ANT)":
                        # Set number of blocks for ANT
                        antTask = ant.ANT(self.pygame_screen, blocks=3)
                        # Run ANT
                        self.antData = antTask.run()
                        # Save ANT data to excel
                        self.antData.to_excel(self.writer, 'ANT', index=False)
                    elif task == "Mental Rotation Task":
                        mrtTask = mrt.MRT(self.pygame_screen)
                        # Run MRT
                        self.mrtData = mrtTask.run()
                        # Save MRT data to excel
                        self.mrtData.to_excel(self.writer, 'MRT', index=False)
                    elif task == "Sustained Attention to Response Task (SART)":
                        sartTask = sart.SART(self.pygame_screen)
                        # Run SART
                        self.sartData = sartTask.run()
                        # Save SART data to excel
                        self.sartData.to_excel(self.writer, 'SART',
                                               index=False)
                    elif task == "Digit Span (backwards)":
                        digitspanBackwardsTask = \
                            digitspan_backwards.DigitspanBackwards(
                                self.pygame_screen)
                        # Run Digit span (Backwards)
                        self.digitspanBackwardsData = digitspanBackwardsTask.run()
                        # Save digit span (backwards) data to excel
                        self.digitspanBackwardsData.to_excel(self.writer,
                                                             'Digit span (backwards)',
                                                             index=False)
                    elif task == "Raven's Progressive Matrices":
                        ravensTask = ravens.Ravens(self.pygame_screen,
                                                   start=9, numTrials=12)
                        # Run Raven's Matrices
                        self.ravensData = ravensTask.run()
                        # Save ravens data to excel
                        self.ravensData.to_excel(self.writer,
                                                 'Ravens Matrices',
                                                 index=False)
                    elif task == "Sternberg Task":
                        sternbergTask = sternberg.Sternberg(self.pygame_screen)
                        # Run Sternberg Task
                        self.sternbergData = sternbergTask.run()
                        # Save sternberg data to excel
                        self.sternbergData.to_excel(self.writer, 'Sternberg',
                                                    index=False)

                    # Save excel file
                    self.writer.save()

                # End of experiment screen
                background = pygame.Surface(self.pygame_screen.get_size())
                background = background.convert()
                background.fill((255, 255, 255))
                pygame.display.set_caption("End of Experiment")
                pygame.mouse.set_visible(1)

                self.pygame_screen.blit(background, (0, 0))

                font = pygame.font.SysFont("arial", 30)
                display.text(self.pygame_screen, font, "End of Experiment",
                             "center", "center")

                pygame.display.flip()

                end_experiment = True
                while end_experiment:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN and \
                                        event.key == pygame.K_SPACE:
                            end_experiment = False

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
