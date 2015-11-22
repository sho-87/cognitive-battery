import sys
import os
import random
import datetime
import pandas as pd
import ant
import mrt
import sart
import ravens
import digitspan_backwards
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_batterySelect(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)

        #get current directory
        self.directory = os.path.dirname(os.path.realpath(__file__))

        #make data folder if it doesnt exist
        self.dataPath = self.directory + "\data\\"
        if not os.path.isdir(self.dataPath):
            os.makedirs(self.dataPath)

        #get list of existing experiment names/IDs currently in use
        self.tempNames = []
        for file in os.listdir(self.dataPath):
            if file.endswith(".xls"):
                self.tempNames.append(file.split("_")[0])

        self.expNames = list(set(self.tempNames))

        self.setupUi(self)

    #add the UI elements for the battery load window
    def setupUi(self, batterySelect):
        batterySelect.setObjectName(_fromUtf8("batterySelect"))
        batterySelect.resize(513, 567)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(batterySelect.sizePolicy().hasHeightForWidth())
        batterySelect.setSizePolicy(sizePolicy)
        batterySelect.setAutoFillBackground(False)
        self.verticalLayout = QtGui.QVBoxLayout(batterySelect)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.mainLayout = QtGui.QVBoxLayout()
        self.mainLayout.setObjectName(_fromUtf8("mainLayout"))
        self.sessionInfoLayout = QtGui.QVBoxLayout()
        self.sessionInfoLayout.setObjectName(_fromUtf8("sessionInfoLayout"))
        self.sessionInfoText = QtGui.QLabel(batterySelect)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sessionInfoText.sizePolicy().hasHeightForWidth())
        self.sessionInfoText.setSizePolicy(sizePolicy)
        self.sessionInfoText.setTextFormat(QtCore.Qt.AutoText)
        self.sessionInfoText.setObjectName(_fromUtf8("sessionInfoText"))
        self.sessionInfoLayout.addWidget(self.sessionInfoText)
        self.sessionInfoColumnLayout = QtGui.QHBoxLayout()
        self.sessionInfoColumnLayout.setObjectName(_fromUtf8("sessionInfoColumnLayout"))
        self.sessionInfoLabelLayout = QtGui.QVBoxLayout()
        self.sessionInfoLabelLayout.setObjectName(_fromUtf8("sessionInfoLabelLayout"))
        self.raText = QtGui.QLabel(batterySelect)
        self.raText.setObjectName(_fromUtf8("raText"))
        self.sessionInfoLabelLayout.addWidget(self.raText)
        self.subNumText = QtGui.QLabel(batterySelect)
        self.subNumText.setObjectName(_fromUtf8("subNumText"))
        self.sessionInfoLabelLayout.addWidget(self.subNumText)
        self.experimentIDText = QtGui.QLabel(batterySelect)
        self.experimentIDText.setObjectName(_fromUtf8("experimentIDText"))
        self.sessionInfoLabelLayout.addWidget(self.experimentIDText)
        self.conditionText = QtGui.QLabel(batterySelect)
        self.conditionText.setObjectName(_fromUtf8("conditionText"))
        self.sessionInfoLabelLayout.addWidget(self.conditionText)
        self.ageText = QtGui.QLabel(batterySelect)
        self.ageText.setObjectName(_fromUtf8("ageText"))
        self.sessionInfoLabelLayout.addWidget(self.ageText)
        self.sexText = QtGui.QLabel(batterySelect)
        self.sexText.setObjectName(_fromUtf8("sexText"))
        self.sessionInfoLabelLayout.addWidget(self.sexText)
        self.sessionInfoColumnLayout.addLayout(self.sessionInfoLabelLayout)
        self.sessionInfoInputLayout = QtGui.QVBoxLayout()
        self.sessionInfoInputLayout.setObjectName(_fromUtf8("sessionInfoInputLayout"))
        self.raBox = QtGui.QLineEdit(batterySelect)
        self.raBox.setObjectName(_fromUtf8("raBox"))
        self.sessionInfoInputLayout.addWidget(self.raBox)
        self.subNumBox = QtGui.QLineEdit(batterySelect)
        self.subNumBox.setObjectName(_fromUtf8("subNumBox"))
        self.sessionInfoInputLayout.addWidget(self.subNumBox)
        self.experimentIDBox = QtGui.QLineEdit(batterySelect)
        self.experimentIDBox.setObjectName(_fromUtf8("experimentIDBox"))
        self.sessionInfoInputLayout.addWidget(self.experimentIDBox)
        self.conditionBox = QtGui.QLineEdit(batterySelect)
        self.conditionBox.setObjectName(_fromUtf8("conditionBox"))
        self.sessionInfoInputLayout.addWidget(self.conditionBox)
        self.ageBox = QtGui.QLineEdit(batterySelect)
        self.ageBox.setObjectName(_fromUtf8("ageBox"))
        self.sessionInfoInputLayout.addWidget(self.ageBox)
        self.sexLayout = QtGui.QHBoxLayout()
        self.sexLayout.setContentsMargins(-1, -1, -1, 0)
        self.sexLayout.setObjectName(_fromUtf8("sexLayout"))
        self.maleRadio = QtGui.QRadioButton(batterySelect)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.maleRadio.sizePolicy().hasHeightForWidth())
        self.maleRadio.setSizePolicy(sizePolicy)
        self.maleRadio.setObjectName(_fromUtf8("maleRadio"))
        self.sexLayout.addWidget(self.maleRadio)
        self.femaleRadio = QtGui.QRadioButton(batterySelect)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.femaleRadio.sizePolicy().hasHeightForWidth())
        self.femaleRadio.setSizePolicy(sizePolicy)
        self.femaleRadio.setObjectName(_fromUtf8("femaleRadio"))
        self.sexLayout.addWidget(self.femaleRadio)
        self.sessionInfoInputLayout.addLayout(self.sexLayout)
        self.sessionInfoColumnLayout.addLayout(self.sessionInfoInputLayout)
        self.sessionInfoLayout.addLayout(self.sessionInfoColumnLayout)
        self.mainLayout.addLayout(self.sessionInfoLayout)
        self.sessionLine = QtGui.QFrame(batterySelect)
        self.sessionLine.setLineWidth(1)
        self.sessionLine.setFrameShape(QtGui.QFrame.HLine)
        self.sessionLine.setFrameShadow(QtGui.QFrame.Sunken)
        self.sessionLine.setObjectName(_fromUtf8("sessionLine"))
        self.mainLayout.addWidget(self.sessionLine)
        self.batteryLayout = QtGui.QVBoxLayout()
        self.batteryLayout.setObjectName(_fromUtf8("batteryLayout"))
        self.batterySelectText = QtGui.QLabel(batterySelect)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.batterySelectText.sizePolicy().hasHeightForWidth())
        self.batterySelectText.setSizePolicy(sizePolicy)
        self.batterySelectText.setScaledContents(True)
        self.batterySelectText.setObjectName(_fromUtf8("batterySelectText"))
        self.batteryLayout.addWidget(self.batterySelectText)
        self.taskOrderLayout = QtGui.QHBoxLayout()
        self.taskOrderLayout.setContentsMargins(-1, -1, -1, 10)
        self.taskOrderLayout.setObjectName(_fromUtf8("taskOrderLayout"))
        self.reorderText = QtGui.QLabel(batterySelect)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.reorderText.setFont(font)
        self.reorderText.setObjectName(_fromUtf8("reorderText"))
        self.taskOrderLayout.addWidget(self.reorderText)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.taskOrderLayout.addItem(spacerItem)
        self.randomOrderCheck = QtGui.QCheckBox(batterySelect)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.randomOrderCheck.sizePolicy().hasHeightForWidth())
        self.randomOrderCheck.setSizePolicy(sizePolicy)
        self.randomOrderCheck.setChecked(False)
        self.randomOrderCheck.setObjectName(_fromUtf8("randomOrderCheck"))
        self.taskOrderLayout.addWidget(self.randomOrderCheck)
        self.batteryLayout.addLayout(self.taskOrderLayout)
        self.selectionLayout = QtGui.QHBoxLayout()
        self.selectionLayout.setContentsMargins(-1, -1, -1, 10)
        self.selectionLayout.setObjectName(_fromUtf8("selectionLayout"))
        spacerItem1 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.selectionLayout.addItem(spacerItem1)
        self.selectAllButton = QtGui.QPushButton(batterySelect)
        self.selectAllButton.setObjectName(_fromUtf8("selectAllButton"))
        self.selectionLayout.addWidget(self.selectAllButton)
        self.deselectAllButton = QtGui.QPushButton(batterySelect)
        self.deselectAllButton.setObjectName(_fromUtf8("deselectAllButton"))
        self.selectionLayout.addWidget(self.deselectAllButton)
        self.batteryLayout.addLayout(self.selectionLayout)
        self.taskListLayout = QtGui.QHBoxLayout()
        self.taskListLayout.setContentsMargins(-1, -1, -1, 0)
        self.taskListLayout.setObjectName(_fromUtf8("taskListLayout"))
        self.taskList = QtGui.QListWidget(batterySelect)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.taskList.setFont(font)
        self.taskList.setProperty("showDropIndicator", False)
        self.taskList.setDragEnabled(True)
        self.taskList.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.taskList.setDefaultDropAction(QtCore.Qt.MoveAction)
        self.taskList.setAlternatingRowColors(True)
        self.taskList.setMovement(QtGui.QListView.Snap)
        self.taskList.setObjectName(_fromUtf8("taskList"))
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.taskList.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.taskList.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Checked)
        self.taskList.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.taskList.addItem(item)
        item = QtGui.QListWidgetItem()
        item.setCheckState(QtCore.Qt.Unchecked)
        self.taskList.addItem(item)
        self.taskListLayout.addWidget(self.taskList)
        self.reorderButtonLayout = QtGui.QVBoxLayout()
        self.reorderButtonLayout.setContentsMargins(0, -1, -1, -1)
        self.reorderButtonLayout.setSpacing(6)
        self.reorderButtonLayout.setObjectName(_fromUtf8("reorderButtonLayout"))
        spacerItem2 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.reorderButtonLayout.addItem(spacerItem2)
        self.upButton = QtGui.QPushButton(batterySelect)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.upButton.sizePolicy().hasHeightForWidth())
        self.upButton.setSizePolicy(sizePolicy)
        self.upButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.upButton.setObjectName(_fromUtf8("upButton"))
        self.reorderButtonLayout.addWidget(self.upButton)
        self.downButton = QtGui.QPushButton(batterySelect)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.downButton.sizePolicy().hasHeightForWidth())
        self.downButton.setSizePolicy(sizePolicy)
        self.downButton.setMaximumSize(QtCore.QSize(50, 16777215))
        self.downButton.setObjectName(_fromUtf8("downButton"))
        self.reorderButtonLayout.addWidget(self.downButton)
        spacerItem3 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.reorderButtonLayout.addItem(spacerItem3)
        self.taskListLayout.addLayout(self.reorderButtonLayout)
        self.batteryLayout.addLayout(self.taskListLayout)
        self.mainLayout.addLayout(self.batteryLayout)
        self.saveLoadLayout = QtGui.QHBoxLayout()
        self.saveLoadLayout.setObjectName(_fromUtf8("saveLoadLayout"))
        self.startButton = QtGui.QPushButton(batterySelect)
        self.startButton.setObjectName(_fromUtf8("startButton"))
        self.saveLoadLayout.addWidget(self.startButton)
        self.cancelButton = QtGui.QPushButton(batterySelect)
        self.cancelButton.setObjectName(_fromUtf8("cancelButton"))
        self.saveLoadLayout.addWidget(self.cancelButton)
        self.mainLayout.addLayout(self.saveLoadLayout)
        self.verticalLayout.addLayout(self.mainLayout)

        #autocomplete for experiment name/ID
        self.experiments = QtCore.QString(';'.join(self.expNames)).split(";")
        self.completer = QtGui.QCompleter(self.experiments, self.experimentIDBox)
        self.experimentIDBox.setCompleter(self.completer)

        self.retranslateUi(batterySelect)
        QtCore.QMetaObject.connectSlotsByName(batterySelect)

    def retranslateUi(self, batterySelect):
        batterySelect.setWindowTitle(_translate("batterySelect", "Cognitive Battery", None))
        self.sessionInfoText.setText(_translate("batterySelect", "<html><head/><body><p><span style=\" font-weight:600;\">Session information:</span></p></body></html>", None))
        self.raText.setText(_translate("batterySelect", "Research Assistant:", None))
        self.subNumText.setText(_translate("batterySelect", "Subject #:", None))
        self.experimentIDText.setText(_translate("batterySelect", "Experiment ID:", None))
        self.conditionText.setText(_translate("batterySelect", "Condition:", None))
        self.ageText.setText(_translate("batterySelect", "Age:", None))
        self.sexText.setText(_translate("batterySelect", "Sex:", None))
        self.maleRadio.setText(_translate("batterySelect", "Male", None))
        self.femaleRadio.setText(_translate("batterySelect", "Female", None))
        self.batterySelectText.setText(_translate("batterySelect", "<html><head/><body><p><span style=\" font-weight:600;\">Task selection:</span></p></body></html>", None))
        self.reorderText.setText(_translate("batterySelect", "(use the Up/Down buttons to set adminstration order)", None))
        self.randomOrderCheck.setText(_translate("batterySelect", "Random order", None))
        self.selectAllButton.setText(_translate("batterySelect", "Select All", None))
        self.deselectAllButton.setText(_translate("batterySelect", "Deselect All", None))
        __sortingEnabled = self.taskList.isSortingEnabled()
        self.taskList.setSortingEnabled(False)
        item = self.taskList.item(0)
        item.setText(_translate("batterySelect", "Attention Network Test (ANT)", None))
        item = self.taskList.item(1)
        item.setText(_translate("batterySelect", "Sustained Attention to Response Task (SART)", None))
        item = self.taskList.item(2)
        item.setText(_translate("batterySelect", "Digit Span (backwards)", None))
        item = self.taskList.item(3)
        item.setText(_translate("batterySelect", "Mental Rotation Task", None))
        item = self.taskList.item(4)
        item.setText(_translate("batterySelect", "Raven\'s Progressive Matrices", None))
        self.taskList.setSortingEnabled(__sortingEnabled)
        self.upButton.setText(_translate("batterySelect", "Up", None))
        self.downButton.setText(_translate("batterySelect", "Down", None))
        self.startButton.setText(_translate("batterySelect", "Start", None))
        self.cancelButton.setText(_translate("batterySelect", "Cancel", None))

        #bind button events
        self.cancelButton.clicked.connect(self.close)
        self.startButton.clicked.connect(self.start)
        self.selectAllButton.clicked.connect(self.selectAll)
        self.deselectAllButton.clicked.connect(self.deselectAll)
        self.upButton.clicked.connect(self.moveUp)
        self.downButton.clicked.connect(self.moveDown)

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
        #store input values
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

        #check for required inputs
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
            #get *selected* tasks and task order
            self.tasks = []
            for index in range(self.taskList.count()):
                #state 2 is selected
                if self.taskList.item(index).checkState() == 2:
                    #add selected task to task list
                    self.tasks.append(str(self.taskList.item(index).text()))

            #check to see if a random order is desired. If so, shuffle tasks
            if self.randomOrderCheck.isChecked():
                random.shuffle(self.tasks)

            #store subject info into a dataframe
            self.subjectInfo = pd.DataFrame(
                data=[(str(self.datetime), str(self.subNum), str(self.experimentID), str(self.condition), int(self.age), str(self.sex), str(self.ra), ', '.join(self.tasks))],
                columns=['datetime', 'subNum', 'expID', 'condition', 'age', 'sex', 'RA', 'tasks']
            )
            #set the output file name
            self.datafileName = "%s_%s_%s.xls" % (self.experimentID, self.subNum, self.condition)

            #check if file already exists
            if os.path.isfile(self.dataPath + self.datafileName):
                self.errorDialog('Data file already exists!')
            else:
                #create the excel writer object and save the file
                self.writer = pd.ExcelWriter(self.dataPath + self.datafileName)
                self.subjectInfo.to_excel(self.writer, 'info', index=False)
                self.writer.save()

                #run each task. return and save their output to dataframe/excel
                for task in self.tasks:
                    if task == "Attention Network Test (ANT)":
                        #set number of blocks for ANT
                        antTask = ant.ANT(blocks = 3)
                        #run ANT
                        self.antData = antTask.run()
                        #save ANT data to excel
                        self.antData.to_excel(self.writer, 'ANT', index=False)
                        print "- ANT complete"
                    elif task == "Mental Rotation Task":
                        mrtTask = mrt.MRT()
                        #run MRT
                        self.mrtData = mrtTask.run()
                        #save MRT data to excel
                        self.mrtData.to_excel(self.writer, 'MRT', index=False)
                        print "- MRT complete"
                    elif task == "Sustained Attention to Response Task (SART)":
                        sartTask = sart.SART()
                        #run SART
                        self.sartData = sartTask.run()
                        #save SART dataB to excel
                        self.sartData.to_excel(self.writer, 'SART', index=False)
                        print "- SART complete"
                    elif task == "Digit Span (backwards)":
                        digitspanBackwardsTask = digitspan_backwards.DigitspanBackwards()
                        #run Digit span (Backwards)
                        self.digitspanBackwardsData = digitspanBackwardsTask.run()
                        #save digit span (backwards) data to excel
                        self.digitspanBackwardsData.to_excel(self.writer, 'Digit span (backwards)', index=False)
                        print "- Digit span (backwards) complete"
                    elif task == "Raven's Progressive Matrices":
                        ravensTask = ravens.Ravens(start = 9, numTrials = 12)
                        #run Raven's Matrices
                        self.ravensData = ravensTask.run()
                        #save ravens data to excel
                        self.ravensData.to_excel(self.writer, 'Ravens Matrices', index=False)
                        print "- Raven's Progressive Matrices complete"

                    #save excel file
                    self.writer.save()

                print "--- Experiment complete"
                self.close()

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    loadScreen = Ui_batterySelect()
    loadScreen.show()
    sys.exit(app.exec_())
