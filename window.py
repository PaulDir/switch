# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'window.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Mainwindow(object):
    def setupUi(self, Mainwindow):
        Mainwindow.setObjectName("Mainwindow")
        Mainwindow.resize(1001, 746)
        self.centralwidget = QtWidgets.QWidget(Mainwindow)
        self.centralwidget.setObjectName("centralwidget")
        self.addSwitch = QtWidgets.QPushButton(self.centralwidget)
        self.addSwitch.setGeometry(QtCore.QRect(140, 140, 93, 28))
        self.addSwitch.setObjectName("addSwitch")
        Mainwindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Mainwindow)
        self.statusbar.setObjectName("statusbar")
        Mainwindow.setStatusBar(self.statusbar)

        self.retranslateUi(Mainwindow)
        QtCore.QMetaObject.connectSlotsByName(Mainwindow)

    def retranslateUi(self, Mainwindow):
        _translate = QtCore.QCoreApplication.translate
        Mainwindow.setWindowTitle(_translate("Mainwindow", "MainWindow"))
        self.addSwitch.setText(_translate("Mainwindow", "PushButton"))
