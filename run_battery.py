import sys
import os
import random
import datetime
import pandas as pd
import PyQt4.QtCore as QtCore
import PyQt4.QtGui as QtGui

import about_dialog

from interface import battery_window_qt
from tasks import ant, mrt, sart, ravens, digitspan_backwards


class BatteryWindow(QtGui.QMainWindow, battery_window_qt.Ui_CognitiveBattery):
    # TODO move this class to a separate file
    def __init__(self):
        super(BatteryWindow, self).__init__()

        # Setup the main window UI
        self.setupUi(self)

        # Initialize the about dialog object
        self.about = None

        # Get current directory
        self.directory = os.path.dirname(os.path.realpath(__file__))

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
        self.actionDocumentation.triggered.connect(self.show_documentation)
        self.actionLicense.triggered.connect(self.show_license)
        self.actionContribute.triggered.connect(self.show_contribute)
        self.actionBrowse_Issues.triggered.connect(self.show_browse_issues)
        self.actionAbout.triggered.connect(self.show_about)

        # TODO disable Up/Down buttons if order is random
        # Bind button events
        self.cancelButton.clicked.connect(self.close)
        self.startButton.clicked.connect(self.start)
        self.selectAllButton.clicked.connect(self.selectAll)
        self.deselectAllButton.clicked.connect(self.deselectAll)
        self.upButton.clicked.connect(self.moveUp)
        self.downButton.clicked.connect(self.moveDown)

    # Open web browser to the documentation page
    def show_documentation(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://github.com/sho-87/cognitive-battery"))

    # Open web browser to the license page
    def show_license(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://github.com/sho-87/cognitive-battery/blob/master/LICENSE"))

    # Open web browser to the github develop branch for contribution
    def show_contribute(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://github.com/sho-87/cognitive-battery/tree/develop"))

    # Open web browser to the github issues page
    def show_browse_issues(self):
        QtGui.QDesktopServices.openUrl(QtCore.QUrl("https://github.com/sho-87/cognitive-battery/issues"))

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

    def errorDialog(self, message):
        QtGui.QMessageBox.warning(self, 'Error', message)

    def selectAll(self):
        for index in range(self.taskList.count()):
            self.taskList.item(index).setCheckState(2)

    def deselectAll(self):
        for index in range(self.taskList.count()):
            self.taskList.item(index).setCheckState(0)

    def moveUp(self):
        currentRow = self.taskList.currentRow()
        currentItem = self.taskList.takeItem(currentRow)
        self.taskList.insertItem(currentRow - 1, currentItem)
        self.taskList.setCurrentItem(currentItem)

    def moveDown(self):
        currentRow = self.taskList.currentRow()
        currentItem = self.taskList.takeItem(currentRow)
        self.taskList.insertItem(currentRow + 1, currentItem)
        self.taskList.setCurrentItem(currentItem)

    def close(self):
        QtCore.QCoreApplication.instance().quit()

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

        # Check for required inputs
        if not self.ra:
            self.errorDialog('Please enter RA name...')
        elif not self.subNum:
            self.errorDialog('Please enter a subject number...')
        elif not self.experimentID:
            self.errorDialog('Please enter an experiment ID...')
        elif not self.condition:
            self.errorDialog('Please enter a condition number...')
        elif not self.age:
            self.errorDialog('Please enter an age...')
        elif not self.maleRadio.isChecked() and not self.femaleRadio.isChecked():
            self.errorDialog('Please select a sex...')
        else:
            # Get *selected* tasks and task order
            self.tasks = []
            for index in range(self.taskList.count()):
                # State 2 is set when item is selected
                if self.taskList.item(index).checkState() == 2:
                    # Add selected task to task list
                    self.tasks.append(str(self.taskList.item(index).text()))

            # Check to see if a random order is desired
            # If so, shuffle tasks
            if self.randomOrderCheck.isChecked():
                random.shuffle(self.tasks)

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
            if os.path.isfile(self.dataPath + self.datafileName):
                self.errorDialog('Data file already exists!')
            else:
                # TODO save each experiment data to their own directory
                # Create the excel writer object and save the file
                self.writer = pd.ExcelWriter(self.dataPath + self.datafileName)
                self.subjectInfo.to_excel(self.writer, 'info', index=False)
                self.writer.save()

                # Run each task
                # Return and save their output to dataframe/excel
                # TODO move data saving to end of each individual task module
                for task in self.tasks:
                    if task == "Attention Network Test (ANT)":
                        # Set number of blocks for ANT
                        antTask = ant.ANT(blocks=3)
                        # Run ANT
                        self.antData = antTask.run()
                        # Save ANT data to excel
                        self.antData.to_excel(self.writer, 'ANT', index=False)
                        print "- ANT complete"
                    elif task == "Mental Rotation Task":
                        mrtTask = mrt.MRT()
                        # Run MRT
                        self.mrtData = mrtTask.run()
                        # Save MRT data to excel
                        self.mrtData.to_excel(self.writer, 'MRT', index=False)
                        print "- MRT complete"
                    elif task == "Sustained Attention to Response Task (SART)":
                        sartTask = sart.SART()
                        # Run SART
                        self.sartData = sartTask.run()
                        # Save SART data to excel
                        self.sartData.to_excel(self.writer, 'SART', index=False)
                        print "- SART complete"
                    elif task == "Digit Span (backwards)":
                        digitspanBackwardsTask = digitspan_backwards.DigitspanBackwards()
                        # Run Digit span (Backwards)
                        self.digitspanBackwardsData = digitspanBackwardsTask.run()
                        # Save digit span (backwards) data to excel
                        self.digitspanBackwardsData.to_excel(self.writer, 'Digit span (backwards)', index=False)
                        print "- Digit span (backwards) complete"
                    elif task == "Raven's Progressive Matrices":
                        ravensTask = ravens.Ravens(start=9, numTrials=12)
                        # Run Raven's Matrices
                        self.ravensData = ravensTask.run()
                        # Save ravens data to excel
                        self.ravensData.to_excel(self.writer, 'Ravens Matrices', index=False)
                        print "- Raven's Progressive Matrices complete"

                    # Save excel file
                    self.writer.save()

                print "--- Experiment complete"
                self.close()


def main():
    # Create main app window
    app = QtGui.QApplication(sys.argv)
    battery_window = BatteryWindow()
    battery_window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
