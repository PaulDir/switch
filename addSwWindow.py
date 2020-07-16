# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addSwWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_addSw2Sw(object):
    def setupUi(self, addSw2Sw):
        addSw2Sw.setObjectName("addSw2Sw")
        addSw2Sw.resize(232, 105)
        self.addBtn = QtWidgets.QPushButton(addSw2Sw)
        self.addBtn.setGeometry(QtCore.QRect(80, 60, 121, 28))
        self.addBtn.setObjectName("addBtn")
        self.label = QtWidgets.QLabel(addSw2Sw)
        self.label.setGeometry(QtCore.QRect(10, 10, 131, 41))
        self.label.setObjectName("label")
        self.linkEdit = QtWidgets.QLineEdit(addSw2Sw)
        self.linkEdit.setGeometry(QtCore.QRect(90, 20, 113, 21))
        self.linkEdit.setObjectName("linkEdit")

        self.retranslateUi(addSw2Sw)
        QtCore.QMetaObject.connectSlotsByName(addSw2Sw)

    def retranslateUi(self, addSw2Sw):
        _translate = QtCore.QCoreApplication.translate
        addSw2Sw.setWindowTitle(_translate("addSw2Sw", "Form"))
        self.addBtn.setText(_translate("addSw2Sw", "添加交换机节点"))
        self.label.setText(_translate("addSw2Sw", "连接端口"))
        self.linkEdit.setText(_translate("addSw2Sw", "0:1"))
