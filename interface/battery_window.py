import os
import sys
import random
import datetime
import pygame
import pandas as pd

from PyQt5 import QtCore, QtGui, QtWidgets
from utils import display, values
from designer import battery_window_qt
from interface import about_dialog, settings_window
from tasks import ant, flanker, mrt, sart, ravens, digitspan_backwards, sternberg


class BatteryWindow(QtWidgets.QMainWindow, battery_window_qt.Ui_CognitiveBattery):
    def __init__(self, base_dir, project_dir, res_width, res_height):
        super(BatteryWindow, self).__init__()

        # Setup the main window UI
        self.setupUi(self)

        # Set app icon
        self.setWindowIcon(QtGui.QIcon(os.path.join("images", "icon_sml.png")))

        self.github_icon = os.path.join("images", "github_icon.png")
        self.actionDocumentation.setIcon(QtGui.QIcon(self.github_icon))
        self.actionLicense.setIcon(QtGui.QIcon(self.github_icon))
        self.actionContribute.setIcon(QtGui.QIcon(self.github_icon))
        self.actionBrowse_Issues.setIcon(QtGui.QIcon(self.github_icon))
        self.actionReport_Bug.setIcon(QtGui.QIcon(self.github_icon))
        self.actionRequest_Feature.setIcon(QtGui.QIcon(self.github_icon))
        self.actionCheck_for_updates.setIcon(QtGui.QIcon(self.github_icon))

        # Get passed values
        self.base_dir = base_dir
        self.project_dir = project_dir
        self.res_width = res_width
        self.res_height = res_height

        # Create/open settings file with no registry fallback  
        self.settings_file = os.path.join(self.project_dir, "battery_settings.ini")
        self.settings = QtCore.QSettings(self.settings_file, QtCore.QSettings.IniFormat)
        self.settings.setFallbacksEnabled(False)

        # Read and save default settings
        self.set_default_settings()

        # Set initial window size/pos from saved settings
        self.settings.beginGroup("MainWindow")
        self.resize(self.settings.value("size"))
        self.move(self.settings.value("pos"))
        self.settings.endGroup()

        # Initialize task settings
        self.task_fullscreen = None
        self.task_borderless = None
        self.task_width = None
        self.task_height = None

        # Keep reference to the about and settings window objects
        self.about = None
        self.settings_window = None

        # Initialize pygame screen
        self.pygame_screen = None

        # Define URLs
        self.links = values.get_links()

        # Make data folder if it doesnt exist
        self.dataPath = os.path.join(self.project_dir, "data")
        if not os.path.isdir(self.dataPath):
            os.makedirs(self.dataPath)

        # Handle menu bar item click events
        self.actionExit.triggered.connect(self.close)
        self.actionSettings.triggered.connect(self.show_settings)
        self.actionDocumentation.triggered.connect(self.show_documentation)
        self.actionLicense.triggered.connect(self.show_license)
        self.actionContribute.triggered.connect(self.show_contribute)
        self.actionBrowse_Issues.triggered.connect(self.show_browse_issues)
        self.actionReport_Bug.triggered.connect(self.show_new_issue)
        self.actionRequest_Feature.triggered.connect(self.show_new_issue)
        self.actionCheck_for_updates.triggered.connect(self.show_releases)
        self.actionAbout.triggered.connect(self.show_about)

        # Bind button events
        self.cancelButton.clicked.connect(self.close)
        self.startButton.clicked.connect(self.start)
        self.randomOrderCheck.clicked.connect(self.random_order_selected)
        self.selectAllButton.clicked.connect(self.select_all)
        self.deselectAllButton.clicked.connect(self.deselect_all)
        self.upButton.clicked.connect(self.move_up)
        self.downButton.clicked.connect(self.move_down)

    # Set default settings values
    def set_default_settings(self):
        """
        Read and save settings values if it exists. Else, write a default value

        This prevents overwriting of existing settings if new task settings are added.
        """

        # Settings - Main Window
        self.settings.beginGroup("MainWindow")
        self.settings.setValue("size", self.settings.value("size", self.size()))
        self.settings.setValue("pos", self.settings.value("pos", QtCore.QPoint(100, 100)))
        self.settings.endGroup()

        # Settings - General
        self.settings.beginGroup("GeneralSettings")
        self.settings.setValue("fullscreen", self.settings.value("fullscreen", "false"))
        self.settings.setValue("borderless", self.settings.value("borderless", "false"))
        self.settings.setValue("width", self.settings.value("width", 1280))
        self.settings.setValue("height", self.settings.value("height", 1024))
        self.settings.setValue("taskBeep", self.settings.value("taskBeep", "true"))
        self.settings.endGroup()

        # Settings - Attention Network Test
        self.settings.beginGroup("AttentionNetworkTest")
        self.settings.setValue("numBlocks", self.settings.value("numBlocks", 3))
        self.settings.endGroup()

        # Settings - Flanker
        self.settings.beginGroup("Flanker")
        self.settings.setValue("darkMode", self.settings.value("darkMode", "false"))
        self.settings.setValue("setsPractice", self.settings.value("setsPractice", 3))
        self.settings.setValue("setsMain", self.settings.value("setsMain", 25))
        self.settings.setValue("blocksCompat", self.settings.value("blocksCompat", 1))
        self.settings.setValue("blocksIncompat", self.settings.value("blocksIncompat", 0))
        self.settings.setValue("blockOrder", self.settings.value("blockOrder", "compatible"))
        self.settings.endGroup()

        # Settings - Ravens
        self.settings.beginGroup("Ravens")
        self.settings.setValue("startImage", self.settings.value("startImage", 13))
        self.settings.setValue("numTrials", self.settings.value("numTrials", 12))
        self.settings.endGroup()

        # Settings - Sternberg Task
        self.settings.beginGroup("Sternberg")
        self.settings.setValue("numBlocks", self.settings.value("numBlocks", 2))
        self.settings.endGroup()

    # Open web browser to the documentation page
    def show_documentation(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.links["github"]))

    # Open web browser to the license page
    def show_license(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.links["license"]))

    # Open web browser to the github develop branch for contribution
    def show_contribute(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.links["develop"]))

    # Open web browser to the github issues page
    def show_browse_issues(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.links["issues"]))

    # Open web browser to the github new issue post
    def show_new_issue(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.links["new_issue"]))

    # Open web browser to the github releases page
    def show_releases(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(self.links["releases"]))

    # Create a new SettingsWindow object and display it
    def show_settings(self):
        # If the settings window does not exist, create one
        if self.settings_window is None:
            self.settings_window = settings_window.SettingsWindow(self, self.settings)
            self.settings_window.show()
            self.settings_window.finished.connect(
                lambda: setattr(self, "settings_window", None))
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
            self.about.finished.connect(lambda: setattr(self, "about", None))
        # If about dialog exists, bring it to the front
        else:
            self.about.activateWindow()
            self.about.raise_()

    def error_dialog(self, message):
        QtWidgets.QMessageBox.warning(self, "Error", message)

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

    def get_settings(self):
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

        self.task_width = int(self.settings.value("width"))
        self.task_height = int(self.settings.value("height"))

        if self.settings.value("taskBeep") == "true":
            self.task_beep = True
        else:
            self.task_beep = False

        self.settings.endGroup()

        # ANT settings
        self.settings.beginGroup("AttentionNetworkTest")
        self.ant_blocks = int(self.settings.value("numBlocks"))
        self.settings.endGroup()

        # Flanker settings
        self.settings.beginGroup("Flanker")
        if self.settings.value("darkMode") == "true":
            self.flanker_dark_mode = True
        else:
            self.flanker_dark_mode = False

        self.flanker_sets_practice = int(self.settings.value("setsPractice"))
        self.flanker_sets_main = int(self.settings.value("setsMain"))
        self.flanker_blocks_compat = int(self.settings.value("blocksCompat"))
        self.flanker_blocks_incompat = int(self.settings.value("blocksIncompat"))
        self.flanker_block_order = str(self.settings.value("blockOrder"))
        self.settings.endGroup()

        # Ravens settings
        self.settings.beginGroup("Ravens")
        self.ravens_start = int(self.settings.value("startImage"))
        self.ravens_trials = int(self.settings.value("numTrials"))
        self.settings.endGroup()

        # Sternberg settings
        self.settings.beginGroup("Sternberg")
        self.sternberg_blocks = int(self.settings.value("numBlocks"))
        self.settings.endGroup()

    # Override the closeEvent method
    def closeEvent(self, event):
        # Save window size and position
        self.settings.beginGroup("MainWindow")
        self.settings.setValue("size", self.size())
        self.settings.setValue("pos", self.pos())
        self.settings.endGroup()

        event.accept()
        sys.exit(0)  # This closes any open pygame windows

    def start(self):
        # Store input values
        sub_num = self.subNumBox.text()
        condition = self.conditionBox.text()
        age = self.ageBox.text()
        ra = self.raBox.text()
        current_date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")

        if self.maleRadio.isChecked():
            sex = "male"
        else:
            sex = "female"

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
            self.error_dialog("No tasks selected")
        elif not ra:
            self.error_dialog("Please enter RA name...")
        elif not sub_num:
            self.error_dialog("Please enter a subject number...")
        elif not condition:
            self.error_dialog("Please enter a condition number...")
        elif not age:
            self.error_dialog("Please enter an age...")
        elif not self.maleRadio.isChecked() and not \
                self.femaleRadio.isChecked():
            self.error_dialog("Please select a sex...")
        else:
            # Store subject info into a dataframe
            subject_info = pd.DataFrame(
                data=[(str(current_date), str(sub_num), str(condition),
                       int(age), str(sex), str(ra),
                       ", ".join(selected_tasks))],
                columns=["datetime", "sub_num", "condition",
                         "age", "sex", "RA", "tasks"]
            )

            # Check if subject number already exists
            existing_subs = [x.split("_")[0] for x in os.listdir(self.dataPath)]
            if sub_num in existing_subs:
                self.error_dialog("Subject number already exists")
            else:
                # Create the excel writer object and save the file
                data_file_name = "%s_%s.xls" % (sub_num, condition)
                output_file = os.path.join(self.dataPath, data_file_name)
                writer = pd.ExcelWriter(output_file)
                subject_info.to_excel(writer, "info", index=False)
                writer.save()

                # Minimize battery UI
                self.showMinimized()

                # Get most recent task settings from file
                self.get_settings()

                # Center all pygame windows if not fullscreen
                if not self.task_fullscreen:
                    pos_x = self.res_width // 2 - self.task_width // 2
                    pos_y = self.res_height // 2 - self.task_height // 2

                    os.environ["SDL_VIDEO_WINDOW_POS"] = \
                        "%s, %s" % (str(pos_x), str(pos_y))

                # Initialize pygame
                pygame.init()

                # Load beep sound
                beep_sound = pygame.mixer.Sound(os.path.join(self.base_dir,
                                                             "tasks",
                                                             "media",
                                                             "beep_med.wav"))

                # Set pygame icon image
                image = os.path.join(self.base_dir, "images", "icon_sml.png")
                icon_img = pygame.image.load(image)
                pygame.display.set_icon(icon_img)

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
                        ant_task = ant.ANT(self.pygame_screen, background, blocks=self.ant_blocks)
                        # Run ANT
                        ant_data = ant_task.run()
                        # Save ANT data to excel
                        ant_data.to_excel(writer, "ANT", index=False)
                    elif task == "Digit Span (backwards)":
                        digitspan_backwards_task = digitspan_backwards.DigitspanBackwards(self.pygame_screen,
                                                                                          background)
                        # Run Digit span (Backwards)
                        digitspan_backwards_data = digitspan_backwards_task.run()
                        # Save digit span (backwards) data to excel
                        digitspan_backwards_data.to_excel(writer, "Digit span (backwards)", index=False)
                    elif task == "Eriksen Flanker Task":
                        flanker_task = flanker.Flanker(self.pygame_screen, background, self.flanker_dark_mode,
                                                       self.flanker_sets_practice, self.flanker_sets_main,
                                                       self.flanker_blocks_compat, self.flanker_blocks_incompat,
                                                       self.flanker_block_order)
                        # Run Eriksen Flanker
                        flanker_data = flanker_task.run()
                        # Save flanker data to excel
                        flanker_data.to_excel(writer, "Eriksen Flanker", index=False)
                    elif task == "Mental Rotation Task":
                        mrt_task = mrt.MRT(self.pygame_screen, background)
                        # Run MRT
                        mrt_data = mrt_task.run()
                        # Save MRT data to excel
                        mrt_data.to_excel(writer, "MRT", index=False)
                    elif task == "Raven's Progressive Matrices":
                        ravens_task = ravens.Ravens(self.pygame_screen, background,
                                                    start=self.ravens_start, numTrials=self.ravens_trials)
                        # Run Raven's Matrices
                        ravens_data = ravens_task.run()
                        # Save ravens data to excel
                        ravens_data.to_excel(writer, "Ravens Matrices", index=False)
                    elif task == "Sternberg Task":
                        sternberg_task = sternberg.Sternberg(self.pygame_screen, background,
                                                             blocks=self.sternberg_blocks)
                        # Run Sternberg Task
                        sternberg_data = sternberg_task.run()
                        # Save sternberg data to excel
                        sternberg_data.to_excel(writer, "Sternberg", index=False)
                    elif task == "Sustained Attention to Response Task (SART)":
                        sart_task = sart.SART(self.pygame_screen, background)
                        # Run SART
                        sart_data = sart_task.run()
                        # Save SART data to excel
                        sart_data.to_excel(writer, "SART", index=False)

                    # Play beep after each task
                    if self.task_beep:
                        beep_sound.play()

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

                print("--- Experiment complete")
                self.close()
