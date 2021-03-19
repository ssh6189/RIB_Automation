# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Result.ui',
# licensing of 'Result.ui' applies.
#
# Created: Wed Mar 17 14:08:51 2021
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Result(object):
    def setupUi(self, Result):
        Result.setObjectName("Result")
        Result.resize(712, 582)
        self.Result_DB1 = QtWidgets.QLabel(Result)
        self.Result_DB1.setGeometry(QtCore.QRect(10, 10, 51, 551))
        self.Result_DB1.setText("")
        self.Result_DB1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.Result_DB1.setWordWrap(False)
        self.Result_DB1.setObjectName("Result_DB1")
        self.Result_DB2 = QtWidgets.QLabel(Result)
        self.Result_DB2.setGeometry(QtCore.QRect(70, 10, 241, 551))
        self.Result_DB2.setText("")
        self.Result_DB2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.Result_DB2.setWordWrap(False)
        self.Result_DB2.setObjectName("Result_DB2")
        self.Result_DB3 = QtWidgets.QLabel(Result)
        self.Result_DB3.setGeometry(QtCore.QRect(320, 10, 381, 551))
        self.Result_DB3.setText("")
        self.Result_DB3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.Result_DB3.setWordWrap(False)
        self.Result_DB3.setObjectName("Result_DB3")

        self.retranslateUi(Result)
        QtCore.QMetaObject.connectSlotsByName(Result)

    def retranslateUi(self, Result):
        Result.setWindowTitle(QtWidgets.QApplication.translate("Result", "Result", None, -1))

