# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Result.ui',
# licensing of 'Result.ui' applies.
#
# Created: Tue Mar 23 11:25:47 2021
#      by: pyside2-uic  running on PySide2 5.13.2
#
# WARNING! All changes made in this file will be lost!

from PySide2 import QtCore, QtGui, QtWidgets

class Ui_Result(object):
    def setupUi(self, Result):
        Result.setObjectName("Result")
        Result.resize(712, 582)
        self.Result_DB1 = QtWidgets.QLabel(Result)
        self.Result_DB1.setGeometry(QtCore.QRect(10, 80, 51, 551))
        self.Result_DB1.setText("")
        self.Result_DB1.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.Result_DB1.setWordWrap(False)
        self.Result_DB1.setObjectName("Result_DB1")
        self.Result_DB2 = QtWidgets.QLabel(Result)
        self.Result_DB2.setGeometry(QtCore.QRect(70, 80, 241, 551))
        self.Result_DB2.setText("")
        self.Result_DB2.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.Result_DB2.setWordWrap(False)
        self.Result_DB2.setObjectName("Result_DB2")
        self.Result_DB3 = QtWidgets.QLabel(Result)
        self.Result_DB3.setGeometry(QtCore.QRect(320, 80, 381, 551))
        self.Result_DB3.setText("")
        self.Result_DB3.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.Result_DB3.setWordWrap(False)
        self.Result_DB3.setObjectName("Result_DB3")
        self.Save = QtWidgets.QPushButton(Result)
        self.Save.setGeometry(QtCore.QRect(20, 10, 75, 23))
        self.Save.setObjectName("Save")
        self.label = QtWidgets.QLabel(Result)
        self.label.setGeometry(QtCore.QRect(10, 50, 56, 12))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Result)
        self.label_2.setGeometry(QtCore.QRect(160, 50, 131, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Result)
        self.label_3.setGeometry(QtCore.QRect(450, 50, 141, 20))
        self.label_3.setObjectName("label_3")

        self.retranslateUi(Result)
        QtCore.QMetaObject.connectSlotsByName(Result)

    def retranslateUi(self, Result):
        Result.setWindowTitle(QtWidgets.QApplication.translate("Result", "Result", None, -1))
        self.Save.setText(QtWidgets.QApplication.translate("Result", "Save", None, -1))
        self.label.setText(QtWidgets.QApplication.translate("Result", "늑근부호", None, -1))
        self.label_2.setText(QtWidgets.QApplication.translate("Result", "늑근 선로길이", None, -1))
        self.label_3.setText(QtWidgets.QApplication.translate("Result", "늑근 개수 / 늑근 사이즈", None, -1))

