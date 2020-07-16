# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Widget.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Widget1(object):
    def setupUi(self, Widget1):
        Widget1.setObjectName("Widget1")
        Widget1.resize(1011, 747)
        self.addSw2SwBtn = QtWidgets.QPushButton(Widget1)
        self.addSw2SwBtn.setGeometry(QtCore.QRect(20, 70, 91, 28))
        self.addSw2SwBtn.setObjectName("addSw2SwBtn")
        self.addMcBtn = QtWidgets.QPushButton(Widget1)
        self.addMcBtn.setGeometry(QtCore.QRect(20, 30, 93, 28))
        self.addMcBtn.setObjectName("addMcBtn")

        self.retranslateUi(Widget1)
        QtCore.QMetaObject.connectSlotsByName(Widget1)

    def retranslateUi(self, Widget1):
        _translate = QtCore.QCoreApplication.translate
        Widget1.setWindowTitle(_translate("Widget1", "Form"))
        self.addSw2SwBtn.setText(_translate("Widget1", "添加交换机"))
        self.addMcBtn.setText(_translate("Widget1", "添加机器"))
