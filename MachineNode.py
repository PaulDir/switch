
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from MachineWindow import *
from switch.machine import *

base=60000


def isValidMac(mac):
    pattern = "[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}"
    return re.fullmatch(pattern, mac)

class SendWin(QWidget):
    def __init__(self,e):
        super().__init__()
        self.ui=Ui_SendWindow()
        self.ui.setupUi(self)
        self.ui.selectBtn.clicked.connect(self.select)
        self.txt=b''
        self.ui.sendBtn.clicked.connect(lambda: e.send(self.ui.macEdit.text(),self.txt))

    def select(self):
        filename = QFileDialog.getOpenFileName(self, 'open file', '')
        with open(filename[0],'rb') as f:
            self.txt=f.read()

    def addmsg(self,msg):
        self.ui.messagebox.insertPlainText(msg)
        self.update()

#机器节点
class MachineNode:
    def __init__(self,x,y,len,wd,port,num,mac,btn,text):
        self.sendWin = SendWin(self)
        self.link=(-1,-1)
        self.machine=Machine(mac,self.sendWin)
        self.width=wd
        self.len=len
        self.setpos(x,y,port)
        self.text=text
        self.btn=btn
        self.btn.setGeometry(self.x,self.y,len,wd)
        self.text.setGeometry(self.x-20, self.y + 80, 150, 38)
        # 设置按钮格式：
        font = QFont()
        font.setBold(True)
        font.setPointSize(8)
        self.btn.setFont(font)
        self.btn.setStyleSheet('QPushButton{background-image:url(pictures/machine.png)}')
        self.btn.setStyleSheet('QPushButton{border-image:url(pictures/machine.png)}')
        self.text.setFont(font)
        _translate = QCoreApplication.translate
        self.text.setText(_translate("MainWindow", "     机器"+str(num))+"\n"+mac)
        self.text.setStyleSheet("border: none")
        #self.text.setStyleSheet("border:none;background: transparent")
        self.btn.clicked.connect(self.goto)


    def link2port(self,pt):
        self.machine.link2port(pt)

    def start(self):
        t=Thread(target=self.machine.work)
        t.start()

    #弹出发送消息界面
    def goto(self):
        self.sendWin.show()

    #发送消息
    def send(self,dest,data):
        if isValidMac(dest):
            #print("send from "+self.machine.mac+" to "+dest+"\n")
            self.machine.send(dest,data)
        else:
            QMessageBox.about(self.sendWin, '', '非法目的Mac地址！')

    def show(self):
        self.btn.show()
        self.text.show()
    #设置制位置

    def setpos(self,x,y,port):
        if port==1:
            self.x,self.y=x-self.len/2,y-self.width
        if port==2:
            self.x,self.y=x-self.len,y-self.width/2
        if port==3:
            self.x,self.y=x-self.len/2,y
        if port==4:
            self.x,self.y=x,y-self.width/2

