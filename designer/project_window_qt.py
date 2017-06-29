# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'project_window_qt.ui'
#
# Created by: PyQt5 UI code generator 5.6
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ProjectWindow(object):
    def setupUi(self, ProjectWindow):
        ProjectWindow.setObjectName("ProjectWindow")
        ProjectWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(ProjectWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.startButton = QtWidgets.QPushButton(self.centralwidget)
        self.startButton.setObjectName("startButton")
        self.horizontalLayout.addWidget(self.startButton)
        self.closeButton = QtWidgets.QPushButton(self.centralwidget)
        self.closeButton.setObjectName("closeButton")
        self.horizontalLayout.addWidget(self.closeButton)
        self.horizontalLayout_2.addLayout(self.horizontalLayout)
        ProjectWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(ProjectWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 21))
        self.menubar.setObjectName("menubar")
        self.menuProject = QtWidgets.QMenu(self.menubar)
        self.menuProject.setObjectName("menuProject")
        ProjectWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(ProjectWindow)
        self.statusbar.setObjectName("statusbar")
        ProjectWindow.setStatusBar(self.statusbar)
        self.actionNewProject = QtWidgets.QAction(ProjectWindow)
        self.actionNewProject.setObjectName("actionNewProject")
        self.actionExit = QtWidgets.QAction(ProjectWindow)
        self.actionExit.setObjectName("actionExit")
        self.menuProject.addAction(self.actionNewProject)
        self.menuProject.addAction(self.actionExit)
        self.menubar.addAction(self.menuProject.menuAction())

        self.retranslateUi(ProjectWindow)
        QtCore.QMetaObject.connectSlotsByName(ProjectWindow)

    def retranslateUi(self, ProjectWindow):
        _translate = QtCore.QCoreApplication.translate
        ProjectWindow.setWindowTitle(_translate("ProjectWindow", "Project Manager"))
        self.startButton.setText(_translate("ProjectWindow", "Start"))
        self.closeButton.setText(_translate("ProjectWindow", "Close"))
        self.menuProject.setTitle(_translate("ProjectWindow", "Project"))
        self.actionNewProject.setText(_translate("ProjectWindow", "New Project"))
        self.actionNewProject.setStatusTip(_translate("ProjectWindow", "Create new project"))
        self.actionExit.setText(_translate("ProjectWindow", "Exit"))
        self.actionExit.setStatusTip(_translate("ProjectWindow", "Exit the battery"))

