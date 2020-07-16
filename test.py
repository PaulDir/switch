import random
import re
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Widget import Ui_Widget1
from addMachineWindow import Ui_addMachineWin
from SendWindow import Ui_SendWindow
from SwitchNode import SwitchNode
from MachineNode import *
from addSw2Sw_Window import*

class Line:
    def __init__(self,x1,y1,x2,y2):
        self.x1=x1
        self.y1=y1
        self.x2=x2
        self.y2=y2

class AddMcWin(QWidget):
    def __init__(self,e):
        super().__init__()
        self.ui=Ui_addMachineWin()
        self.ui.setupUi(self)
        self.ui.addBtn.clicked.connect(e.linkMc2Sw)

class AddSwtoSwWin(QWidget):
    def __init__(self,e):
        super().__init__()
        self.ui=Ui_addSw2Sw()
        self.ui.setupUi(self)
        self.ui.addBtn.clicked.connect(e.linkSw2Sw)

class Test(QWidget):
    def __init__(self):
        super().__init__()
        self.addSw2SwWin=AddSwtoSwWin(self)
        self.addMcWin=AddMcWin(self)
        self.ui=Ui_Widget1()
        self.ui.setupUi(self)
        self.ui.addSw2SwBtn.clicked.connect(self.goto_addSw2Sw)
        self.ui.addMcBtn.clicked.connect(self.goto_addMachine)
        self.switches=[]
        self.machines=[]
        self.lines=[]
        self.initSwitch()

    def paintEvent(self,event):
        painter = QPainter(self)
        pixmap = QPixmap("myPic.png")
        painter.drawPixmap(self.rect(), pixmap)
        pen = QPen(Qt.black, 3)
        pen.setWidth(2)
        painter.setPen(pen)

        for l in self.lines:
            painter.drawLine(l.x1, l.y1, l.x2, l.y2)


    def goto_addMachine(self):
        self.addMcWin.show()


    def isValidMac(sel,mac):
        pattern="[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}"
        return re.fullmatch(pattern,mac)

    #判断 机器-交换机的连接输入是否正确
    def isValidLink1(self,link):
        pattern="[0-9]+:[1-4]"
        return re.fullmatch(pattern,link)

    # 判断 交换机-交换机的连接输入是否正确
    def isValidLink2(self,link):
        pattern="[1-4]-[0-9]+:[1-4]"
        return re.fullmatch(pattern,link)

    def linkMc2Sw(self):
        mac=self.addMcWin.ui.macEdit.text()
        link=self.addMcWin.ui.linkEdit.text()

        if not self.isValidMac(mac):
            QMessageBox.about(self, '', 'mac地址格式错误\n 正确格式：xx:xx:xx:xx\n 上式x为十六进制数')

        elif not self.isValidLink1(link) :
            QMessageBox.about(self, '', 'link格式错误\n 正确格式：x:y\n 上式x为交换机号，y为端口号 \n 端口号为1-4')
        else :
            sw, port = link.split(':')

            if int(sw)>len(self.switches)-1:
                QMessageBox.about(self, '', '交换机号不存在 ')

            else: self.addMc2Sw(mac,int(sw),int(port))
        self.addMcWin.close()

    def addMc2Sw(self,mac,swNum,port):
        x1,y1,x2,y2=self.switches[swNum].port_pos(port)
        l=Line(x1,y1,x2,y2)
        self.lines.append(l)
        machine=MachineNode(x2,y2,100,50,port,mac,QPushButton(self))
        #将机器节点添加到列表中
        self.machines.append(machine)
        _translate = QCoreApplication.translate
        machine.btn.setText(_translate("MainWindow", "机器"+str(len(self.machines)-1)+"\n"+mac))
        machine.show()

        self.update()

    def goto_addSw2Sw(self):
        self.addSw2SwWin.show()

    def linkSw2Sw(self):
        link=self.addSw2SwWin.ui.linkEdit.text()
        if not self.isValidLink1(link) :
            QMessageBox.about(self, '', 'link格式错误\n 正确格式：s:p2\n s,p2为连接到的交换机号/端口号 \n 端口号为1-4')
        else:
            sw, port = link.split(':')
            if int(sw) > len(self.switches) - 1:
                QMessageBox.about(self, '', '交换机号不存在 ')

            else:
                self.addSw(int(sw), int(port))
        self.addSw2SwWin.close()

    def addSw(self,swNum,port):

        x1,y1,x2,y2=self.switches[swNum].port_pos(port)
        l=Line(x1,y1,x2,y2)
        self.lines.append(l)
        sw=SwitchNode(x2,y2,100,50,port,QPushButton(self))
        #将机器节点添加到列表中
        self.switches.append(sw)
        _translate = QCoreApplication.translate
        sw.btn.setText(_translate("MainWindow", "交换机"+str(len(self.switches)-1)))

        sw.show()

        self.update()
    def initSwitch(self):
        swnode=SwitchNode(400,400,100,50,-1,QPushButton(self))
        #将新交换机加入列表
        self.switches.append(swnode)
        _translate = QCoreApplication.translate
        swnode.btn.setText(_translate("MainWindow", "交换机"+str(len(self.switches)-1)))
        swnode.show()

        self.update()


if __name__ == '__main__':
    random.seed(a=None, version=2)
    app = QApplication(sys.argv)
    test = Test()
    test.show()
    sys.exit(app.exec_())