# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'about_dialog_qt.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setWindowModality(QtCore.Qt.ApplicationModal)
        Dialog.resize(396, 156)
        Dialog.setModal(True)
        self.verticalLayout = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.title = QtGui.QLabel(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.title.sizePolicy().hasHeightForWidth())
        self.title.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.title.setFont(font)
        self.title.setAlignment(QtCore.Qt.AlignCenter)
        self.title.setOpenExternalLinks(False)
        self.title.setTextInteractionFlags(QtCore.Qt.LinksAccessibleByMouse)
        self.title.setObjectName(_fromUtf8("title"))
        self.verticalLayout.addWidget(self.title)
        self.mainLayout = QtGui.QHBoxLayout()
        self.mainLayout.setObjectName(_fromUtf8("mainLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.emailLabel = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.emailLabel.setFont(font)
        self.emailLabel.setObjectName(_fromUtf8("emailLabel"))
        self.gridLayout.addWidget(self.emailLabel, 2, 0, 1, 1)
        self.emailValue = QtGui.QLabel(Dialog)
        self.emailValue.setOpenExternalLinks(True)
        self.emailValue.setObjectName(_fromUtf8("emailValue"))
        self.gridLayout.addWidget(self.emailValue, 2, 1, 1, 1)
        self.versionValue = QtGui.QLabel(Dialog)
        self.versionValue.setObjectName(_fromUtf8("versionValue"))
        self.gridLayout.addWidget(self.versionValue, 0, 1, 1, 1)
        self.websiteValue = QtGui.QLabel(Dialog)
        self.websiteValue.setOpenExternalLinks(True)
        self.websiteValue.setObjectName(_fromUtf8("websiteValue"))
        self.gridLayout.addWidget(self.websiteValue, 3, 1, 1, 1)
        self.authorValue = QtGui.QLabel(Dialog)
        self.authorValue.setObjectName(_fromUtf8("authorValue"))
        self.gridLayout.addWidget(self.authorValue, 1, 1, 1, 1)
        self.websiteLabel = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.websiteLabel.setFont(font)
        self.websiteLabel.setObjectName(_fromUtf8("websiteLabel"))
        self.gridLayout.addWidget(self.websiteLabel, 3, 0, 1, 1)
        self.versionLabel = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.versionLabel.setFont(font)
        self.versionLabel.setObjectName(_fromUtf8("versionLabel"))
        self.gridLayout.addWidget(self.versionLabel, 0, 0, 1, 1)
        self.authorLabel = QtGui.QLabel(Dialog)
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.authorLabel.setFont(font)
        self.authorLabel.setObjectName(_fromUtf8("authorLabel"))
        self.gridLayout.addWidget(self.authorLabel, 1, 0, 1, 1)
        self.mainLayout.addLayout(self.gridLayout)
        self.icon = QtGui.QLabel(Dialog)
        self.icon.setText(_fromUtf8(""))
        self.icon.setScaledContents(False)
        self.icon.setAlignment(QtCore.Qt.AlignCenter)
        self.icon.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.icon.setObjectName(_fromUtf8("icon"))
        self.mainLayout.addWidget(self.icon)
        self.verticalLayout.addLayout(self.mainLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "About", None))
        self.title.setText(_translate("Dialog", "Cognitive Battery", None))
        self.emailLabel.setText(_translate("Dialog", "Email:", None))
        self.emailValue.setText(_translate("Dialog", "<a href=\"mailto:simonho213@gmail.com?Subject=Cognitive%20Battery\">simonho213@gmail.com</a>", None))
        self.versionValue.setText(_translate("Dialog", "1.1", None))
        self.websiteValue.setText(_translate("Dialog", "<a href=\"http://www.simonho.ca\">www.simonho.ca</a>", None))
        self.authorValue.setText(_translate("Dialog", "Simon Ho", None))
        self.websiteLabel.setText(_translate("Dialog", "Website:", None))
        self.versionLabel.setText(_translate("Dialog", "Version:", None))
        self.authorLabel.setText(_translate("Dialog", "Author:", None))

