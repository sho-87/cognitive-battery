# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'settings_window_qt.ui'
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

class Ui_SettingsDialog(object):
    def setupUi(self, SettingsDialog):
        SettingsDialog.setObjectName(_fromUtf8("SettingsDialog"))
        SettingsDialog.setWindowModality(QtCore.Qt.ApplicationModal)
        SettingsDialog.resize(350, 171)
        SettingsDialog.setSizeGripEnabled(True)
        SettingsDialog.setModal(True)
        self.verticalLayout_2 = QtGui.QVBoxLayout(SettingsDialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.settings_main_layout = QtGui.QVBoxLayout()
        self.settings_main_layout.setObjectName(_fromUtf8("settings_main_layout"))
        self.settings_scroll_area = QtGui.QScrollArea(SettingsDialog)
        self.settings_scroll_area.setFrameShape(QtGui.QFrame.NoFrame)
        self.settings_scroll_area.setLineWidth(0)
        self.settings_scroll_area.setWidgetResizable(True)
        self.settings_scroll_area.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.settings_scroll_area.setObjectName(_fromUtf8("settings_scroll_area"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 330, 101))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(5, 0, 5, 0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.settings_tasks_group = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.settings_tasks_group.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.settings_tasks_group.setObjectName(_fromUtf8("settings_tasks_group"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.settings_tasks_group)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.settings_task_fullscreen_layout = QtGui.QHBoxLayout()
        self.settings_task_fullscreen_layout.setObjectName(_fromUtf8("settings_task_fullscreen_layout"))
        self.settings_task_maximize_label = QtGui.QLabel(self.settings_tasks_group)
        self.settings_task_maximize_label.setObjectName(_fromUtf8("settings_task_maximize_label"))
        self.settings_task_fullscreen_layout.addWidget(self.settings_task_maximize_label)
        self.settings_task_fullscreen_checkbox = QtGui.QCheckBox(self.settings_tasks_group)
        self.settings_task_fullscreen_checkbox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.settings_task_fullscreen_checkbox.setText(_fromUtf8(""))
        self.settings_task_fullscreen_checkbox.setObjectName(_fromUtf8("settings_task_fullscreen_checkbox"))
        self.settings_task_fullscreen_layout.addWidget(self.settings_task_fullscreen_checkbox)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.settings_task_fullscreen_layout.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.settings_task_fullscreen_layout)
        self.settings_task_size = QtGui.QHBoxLayout()
        self.settings_task_size.setObjectName(_fromUtf8("settings_task_size"))
        self.settings_task_width_label = QtGui.QLabel(self.settings_tasks_group)
        self.settings_task_width_label.setObjectName(_fromUtf8("settings_task_width_label"))
        self.settings_task_size.addWidget(self.settings_task_width_label)
        self.settings_task_width_value = QtGui.QLineEdit(self.settings_tasks_group)
        self.settings_task_width_value.setObjectName(_fromUtf8("settings_task_width_value"))
        self.settings_task_size.addWidget(self.settings_task_width_value)
        self.settings_task_height_label = QtGui.QLabel(self.settings_tasks_group)
        self.settings_task_height_label.setObjectName(_fromUtf8("settings_task_height_label"))
        self.settings_task_size.addWidget(self.settings_task_height_label)
        self.settings_task_height_value = QtGui.QLineEdit(self.settings_tasks_group)
        self.settings_task_height_value.setObjectName(_fromUtf8("settings_task_height_value"))
        self.settings_task_size.addWidget(self.settings_task_height_value)
        self.verticalLayout_3.addLayout(self.settings_task_size)
        self.verticalLayout.addWidget(self.settings_tasks_group)
        self.settings_scroll_area.setWidget(self.scrollAreaWidgetContents)
        self.settings_main_layout.addWidget(self.settings_scroll_area)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.settings_main_layout.addItem(spacerItem1)
        self.settings_button_layout = QtGui.QHBoxLayout()
        self.settings_button_layout.setObjectName(_fromUtf8("settings_button_layout"))
        self.settings_save_button = QtGui.QPushButton(SettingsDialog)
        self.settings_save_button.setAutoDefault(False)
        self.settings_save_button.setObjectName(_fromUtf8("settings_save_button"))
        self.settings_button_layout.addWidget(self.settings_save_button)
        self.settings_cancel_button = QtGui.QPushButton(SettingsDialog)
        self.settings_cancel_button.setAutoDefault(False)
        self.settings_cancel_button.setObjectName(_fromUtf8("settings_cancel_button"))
        self.settings_button_layout.addWidget(self.settings_cancel_button)
        self.settings_main_layout.addLayout(self.settings_button_layout)
        self.verticalLayout_2.addLayout(self.settings_main_layout)

        self.retranslateUi(SettingsDialog)
        QtCore.QMetaObject.connectSlotsByName(SettingsDialog)

    def retranslateUi(self, SettingsDialog):
        SettingsDialog.setWindowTitle(_translate("SettingsDialog", "Settings", None))
        self.settings_tasks_group.setTitle(_translate("SettingsDialog", "Task Windows", None))
        self.settings_task_maximize_label.setText(_translate("SettingsDialog", "Fullscreen:", None))
        self.settings_task_fullscreen_checkbox.setStatusTip(_translate("SettingsDialog", "Show tasks in fullscreen mode", None))
        self.settings_task_width_label.setText(_translate("SettingsDialog", "Width:", None))
        self.settings_task_width_value.setStatusTip(_translate("SettingsDialog", "Width of the task windows", None))
        self.settings_task_height_label.setText(_translate("SettingsDialog", "Height:", None))
        self.settings_task_height_value.setStatusTip(_translate("SettingsDialog", "Height of the task windows", None))
        self.settings_save_button.setStatusTip(_translate("SettingsDialog", "Save settings", None))
        self.settings_save_button.setText(_translate("SettingsDialog", "Save", None))
        self.settings_cancel_button.setStatusTip(_translate("SettingsDialog", "Cancel", None))
        self.settings_cancel_button.setText(_translate("SettingsDialog", "Cancel", None))

