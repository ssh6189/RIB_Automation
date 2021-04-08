# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Save.ui',
# licensing of 'Save.ui' applies.
#
# Created: Tue Mar 23 11:31:30 2021
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Save(object):
    def setupUi(self, Save):
        Save.setObjectName("Save")
        Save.resize(300, 128)
        self.pushButton_1 = QtWidgets.QPushButton(Save)
        self.pushButton_1.setGeometry(QtCore.QRect(40, 70, 75, 23))
        self.pushButton_1.setObjectName("pushButton_1")
        self.pushButton_2 = QtWidgets.QPushButton(Save)
        self.pushButton_2.setGeometry(QtCore.QRect(180, 70, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.label = QtWidgets.QLabel(Save)
        self.label.setGeometry(QtCore.QRect(40, 30, 221, 16))
        self.label.setObjectName("label")

        self.retranslateUi(Save)
        QtCore.QMetaObject.connectSlotsByName(Save)

    def retranslateUi(self, Save):
        Save.setWindowTitle(QtWidgets.QApplication.translate("Save", "Save", None, -1))
        self.pushButton_1.setText(QtWidgets.QApplication.translate("Save", "Yes", None, -1))
        self.pushButton_2.setText(QtWidgets.QApplication.translate("Save", "No", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Save", "결과를 저장하시겠습니까?", None, -1))

