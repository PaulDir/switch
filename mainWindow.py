# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Widget1(object):
    def setupUi(self, Widget1):
        Widget1.setObjectName("Widget1")
        Widget1.resize(1112, 747)
        self.addSw2SwBtn = QtWidgets.QPushButton(Widget1)
        self.addSw2SwBtn.setGeometry(QtCore.QRect(110, 90, 131, 41))
        font = QtGui.QFont()
        font.setFamily("华文行楷")
        font.setPointSize(14)
        font.setUnderline(True)
        self.addSw2SwBtn.setFont(font)
        self.addSw2SwBtn.setObjectName("addSw2SwBtn")
        self.addMcBtn = QtWidgets.QPushButton(Widget1)
        self.addMcBtn.setGeometry(QtCore.QRect(122, 20, 111, 41))
        font = QtGui.QFont()
        font.setFamily("华文行楷")
        font.setPointSize(14)
        font.setUnderline(True)
        self.addMcBtn.setFont(font)
        self.addMcBtn.setObjectName("addMcBtn")
        self.message = QtWidgets.QTextEdit(Widget1)
        self.message.setGeometry(QtCore.QRect(0, 140, 261, 611))
        self.message.setObjectName("message")
        self.background1 = QtWidgets.QTextEdit(Widget1)
        self.background1.setGeometry(QtCore.QRect(0, 0, 261, 141))
        self.background1.setObjectName("background1")
        self.background2 = QtWidgets.QTextEdit(Widget1)
        self.background2.setGeometry(QtCore.QRect(260, 0, 861, 71))
        self.background2.setObjectName("background2")
        self.label = QtWidgets.QLabel(Widget1)
        self.label.setGeometry(QtCore.QRect(540, 20, 271, 41))
        font = QtGui.QFont()
        font.setFamily("华文行楷")
        font.setPointSize(22)
        font.setUnderline(False)
        font.setStrikeOut(False)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.message.raise_()
        self.background1.raise_()
        self.addMcBtn.raise_()
        self.addSw2SwBtn.raise_()
        self.background2.raise_()
        self.label.raise_()

        self.retranslateUi(Widget1)
        QtCore.QMetaObject.connectSlotsByName(Widget1)

    def retranslateUi(self, Widget1):
        _translate = QtCore.QCoreApplication.translate
        Widget1.setWindowTitle(_translate("Widget1", "Form"))
        self.addSw2SwBtn.setText(_translate("Widget1", "添加交换机"))
        self.addMcBtn.setText(_translate("Widget1", "添加机器"))
        self.label.setText(_translate("Widget1", "交换机仿真系统"))
