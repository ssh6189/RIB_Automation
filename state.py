# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'state.ui',
# licensing of 'state.ui' applies.
#
# Created: Fri Apr  2 16:44:14 2021
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Wait(object):
    def setupUi(self, Wait):
        Wait.setObjectName("Wait")
        Wait.resize(393, 168)
        self.label = QtWidgets.QLabel(Wait)
        self.label.setGeometry(QtCore.QRect(50, 30, 291, 21))
        self.label.setObjectName("label")
        self.Left = QtWidgets.QPushButton(Wait)
        self.Left.setGeometry(QtCore.QRect(50, 90, 75, 23))
        self.Left.setObjectName("Left")
        self.Right = QtWidgets.QPushButton(Wait)
        self.Right.setGeometry(QtCore.QRect(270, 90, 75, 23))
        self.Right.setObjectName("Right")
        self.Okay = QtWidgets.QPushButton(Wait)
        self.Okay.setGeometry(QtCore.QRect(160, 130, 75, 23))
        self.Okay.setObjectName("Okay")
        self.Stop = QtWidgets.QPushButton(Wait)
        self.Stop.setGeometry(QtCore.QRect(160, 90, 75, 23))
        self.Stop.setObjectName("Stop")

        self.retranslateUi(Wait)
        QtCore.QMetaObject.connectSlotsByName(Wait)

    def retranslateUi(self, Wait):
        Wait.setWindowTitle(QtWidgets.QApplication.translate("Wait", "Controller", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Wait", "                 기계 상태를 초기화해주세요.", None, -1))
        self.Left.setText(QtWidgets.QApplication.translate("Wait", "<--", None, -1))
        self.Right.setText(QtWidgets.QApplication.translate("Wait", "-->", None, -1))
        self.Okay.setText(QtWidgets.QApplication.translate("Wait", "늑근 가공", None, -1))
        self.Stop.setText(QtWidgets.QApplication.translate("Wait", "Stop", None, -1))

