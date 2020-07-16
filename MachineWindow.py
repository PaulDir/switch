# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MachineWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_SendWindow(object):
    def setupUi(self, SendWindow):
        SendWindow.setObjectName("SendWindow")
        SendWindow.resize(602, 461)
        self.label = QtWidgets.QLabel(SendWindow)
        self.label.setGeometry(QtCore.QRect(20, 20, 101, 16))
        self.label.setObjectName("label")
        self.macEdit = QtWidgets.QLineEdit(SendWindow)
        self.macEdit.setGeometry(QtCore.QRect(110, 20, 113, 21))
        self.macEdit.setObjectName("macEdit")
        self.selectBtn = QtWidgets.QPushButton(SendWindow)
        self.selectBtn.setGeometry(QtCore.QRect(10, 50, 111, 28))
        self.selectBtn.setObjectName("selectBtn")
        self.sendBtn = QtWidgets.QPushButton(SendWindow)
        self.sendBtn.setGeometry(QtCore.QRect(130, 100, 93, 28))
        self.sendBtn.setObjectName("sendBtn")
        self.messagebox = QtWidgets.QTextEdit(SendWindow)
        self.messagebox.setGeometry(QtCore.QRect(230, -4, 381, 471))
        self.messagebox.setObjectName("messagebox")

        self.retranslateUi(SendWindow)
        QtCore.QMetaObject.connectSlotsByName(SendWindow)

    def retranslateUi(self, SendWindow):
        _translate = QtCore.QCoreApplication.translate
        SendWindow.setWindowTitle(_translate("SendWindow", "Form"))
        self.label.setText(_translate("SendWindow", "目的MAC地址"))
        self.selectBtn.setText(_translate("SendWindow", "选择传送文件"))
        self.sendBtn.setText(_translate("SendWindow", "发送"))
