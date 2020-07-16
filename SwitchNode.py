from threading import Thread
import time
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QWidget, QTableWidgetItem

from switch.Switch import  *
from switchWindow import*

class SwWin(QWidget):
    def __init__(self,e):
        super().__init__()
        self.ui=Ui_swWindow()
        self.ui.setupUi(self)
        self.initTable()
        self.ui.background.setStyleSheet("QTextEdit{background-image: url(pictures/back17.jpg);border-image:url(pictures/back17.jpg)}")

    def initTable(self):
        self.ui.addrTable.setColumnCount(3)
        self.ui.addrTable.setRowCount(6)
        self.ui.addrTable.setItem(0, 0, QTableWidgetItem("              MAC地址"))
        self.ui.addrTable.setItem(0, 1, QTableWidgetItem("              端口号"))
        self.ui.addrTable.setItem(0, 2, QTableWidgetItem("              老化时间"))
        for j in range(3):
            self.ui.addrTable.setColumnWidth(j, 198)
        for i in range(5):
            self.ui.addrTable.setRowHeight(i, 35)
        self.ui.addrTable.verticalHeader().setVisible(False)
        self.ui.addrTable.horizontalHeader().setVisible(False)

    def addPortmsg(self,i,msg):
        if i== 0 :
            self.ui.port1Msg.insertPlainText(msg)
        elif i== 1 :
            self.ui.port2Msg.insertPlainText(msg)
        elif i == 2:
            self.ui.port3Msg.insertPlainText(msg)
        elif i == 3:
            self.ui.port4Msg.insertPlainText(msg)

    def updateTableItem(self,index,item):
        if index!=-1:
                self.ui.addrTable.setItem(index+1,0,QTableWidgetItem(item.mac_addr))
                self.ui.addrTable.setItem(index + 1, 1, QTableWidgetItem(str(item.port)))
                self.ui.addrTable.setItem(index + 1, 2, QTableWidgetItem(str(item.timestamp)))


    def updateAge(self):
        for i in range(1,6):
            if self.ui.addrTable.item(i,2):
                timestamp=int(self.ui.addrTable.item(i,2).text())
                timestamp+=1
                self.ui.addrTable.setItem(i, 2, QTableWidgetItem(str(timestamp)))
#交换机节点
class SwitchNode:
    def __init__(self,x,y,len,wd,num,port,btn,text):
        self.links=[False,False,False,False]
        self.window=SwWin(self)
        self.switch=Switch(num,0,self.window)
        self.width=wd
        self.len=len
        self.setpos(x, y, port)
        self.btn=btn
        self.text=text
        self.btn.setGeometry(self.x,self.y,80,80)
        self.text.setGeometry(self.x+5,self.y+80,100,25)
        font = QFont()
        font.setBold(True)
        font.setPointSize(9)
        self.text.setFont(font)
        _translate = QCoreApplication.translate
        self.text.setText(_translate("MainWindow", "交换机"+str(num)))
        self.text.setStyleSheet("border:none;")
        self.btn.setStyleSheet('QPushButton{background-image:url(pictures/switch.png)}')
        self.btn.setStyleSheet('QPushButton{border-image:url(pictures/switch.png)}')
        self.btn.clicked.connect(self.goto)

    def goto(self):
        self.window.show()

    def getport(self,n):
        return self.switch.ports[n-1]
    def setpos(self,x,y,direc):
        if direc==1:
            self.x,self.y=x-self.len/2,y-self.width
        elif direc==2:
            self.x,self.y=x-self.len,y-self.width/2
        elif direc==3:
            self.x,self.y=x-self.len/2,y
        elif direc==4:
            self.x,self.y=x,y-self.width/2
        else:
            self.x,self.y=x,y

    #def setLink(self,my_port,dest_sw,dest_port):
        #self.links[my_port]=(dest_sw,dest_port)

    def show(self):

        self.btn.show()
        self.text.show()
    def port1_pos(self):
        return (self.x+self.len/2-10,self.y,self.x+self.len/2-10,self.y-90)

    def port2_pos(self):
        return (self.x,self.y+self.width/2+5,self.x-70,self.y+self.width/2+5)
    def port3_pos(self):
        return (self.x+self.len/2-10,self.y+self.width/2,self.x+self.len/2-10,self.y+self.width/2+110)
    def port4_pos(self):
        return (self.x+self.len-20,self.y+self.width/2+5, self.x+self.len+70-20,self.y+self.width/2+5)

    def port_pos(self,i):
        if i==1: return self.port1_pos();
        if i==2: return self.port2_pos();
        if i == 3: return self.port3_pos();
        if i == 4: return self.port4_pos();

    def add_activePort(self,i):
        self.switch.add_active_port(i)

