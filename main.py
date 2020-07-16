import random
import re
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from mainWindow import Ui_Widget1
from addMachineWindow import Ui_addMachineWin
from MachineWindow import *
from SwitchNode import SwitchNode
from MachineNode import *
from addSwWindow import*

swCount=0

global message
def start(func):
    t = Thread(target=func)
    t.start()

def adjust(pt,x,y):
    if pt==1 or pt==3: return(x+10,y)
    elif pt==2: return(x+20,y-5)
    elif pt==4: return(x,y-5)
    return (x,y)

def adjust2(pt,x,y):
    if pt==3: return (x-10,y)
    elif pt==1: return (x,y+10)
    elif pt==4: return (x-10,y)
    return (x,y)
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

class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.addSw2SwWin=AddSwtoSwWin(self)
        self.addMcWin=AddMcWin(self)
        self.ui=Ui_Widget1()
        self.ui.setupUi(self)
        self.ui.addSw2SwBtn.clicked.connect(self.goto_addSw2Sw)
        self.ui.addMcBtn.clicked.connect(self.goto_addMachine)
        self.ui.background1.setStyleSheet("background-image: url(pictures/back1.png)")
        self.ui.background2.setStyleSheet("background-image: url(pictures/back1.png)")
        self.ui.message.setStyleSheet("background-image: url(pictures/back14.jpg)")

        self.setStyleSheet("background: white")
        self.ui.label.setStyleSheet("background: transparent")
        self.ui.addSw2SwBtn.setStyleSheet("background: transparent")
        self.ui.addMcBtn.setStyleSheet("background: transparent")

        #self.ui.background1.setStyleSheet("background:blue")
        self.switches=[]
        self.machines=[]
        self.lines=[]
        self.links=[]
        self.initSwitch()
        message=''
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
        pattern="[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}:[A-Fa-f0-9]{2}"
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
            QMessageBox.about(self, '', 'mac地址格式错误\n 正确格式：xx:xx:xx:xx:xx:xx\n 上式x为十六进制数')

        elif not self.isValidLink1(link) :
            QMessageBox.about(self, '', 'link格式错误\n 正确格式：x:y\n 上式x为交换机号，y为端口号 \n 端口号为1:4')
        else :
            swNum, pt = link.split(':')
            swNum=int(swNum)
            pt=int(pt)
            if self.switches[swNum].links[pt-1]:
                QMessageBox.about(self, '', '同一端口，不允许重复连接！')
            elif swNum>len(self.switches)-1:
                QMessageBox.about(self, '', '交换机号不存在 ')
            else:
                self.switches[swNum].links[pt-1]=True
                self.addMachine(mac,swNum,pt)
        self.addMcWin.close()

    def addMachine(self,mac,swNum,pt):
        #mac=''.join(re.split('[:-]', mac))
        sw=self.switches[swNum]
        x1,y1,x2,y2=sw.port_pos(pt)
        if pt==3: y2+=15
        sw=sw.switch
        l=Line(x1,y1,x2,y2)
        self.lines.append(l)
        x2,y2=adjust2(pt,x2,y2)
        #创建新的机器节点，将其连接到目标端口
        machine=MachineNode(x2,y2,80,80,pt,len(self.machines),mac,QPushButton(self),QTextEdit(self))
        machine.link2port(sw.getPort(pt-1))
        sw.ports[pt-1].link2machine()
        sw.add_active_port(pt)
        #启动机器，端口
        machine.start()
        start(sw.ports[pt-1].work)

        #将机器节点添加到列表中
        self.machines.append(machine)

        machine.show()

        self.update()

    def goto_addSw2Sw(self):
        self.addSw2SwWin.show()

    def linkSw2Sw(self):
        link=self.addSw2SwWin.ui.linkEdit.text()
        if not self.isValidLink1(link) :
            QMessageBox.about(self, '', 'link格式错误\n 正确格式：s:p2\n s,p2为连接到的交换机号/端口号 \n 端口号为1-4')
        else:
            sw, pt = link.split(':')
            sw=int(sw)
            pt=int(pt)
            if self.switches[sw].links[pt-1]:
                QMessageBox.about(self, '', '同一端口，不允许重复连接！')
            elif sw > len(self.switches) - 1:
                QMessageBox.about(self, '', '交换机号不存在 ')
            else:
                self.switches[sw].links[pt-1] = True
                self.addSw(sw, pt)
        self.addSw2SwWin.close()

    def addSw(self,swNum,port):
        link_sw=self.switches[swNum]
        x1,y1,x2,y2=link_sw.port_pos(port)
        l=Line(x1,y1,x2,y2)
        self.lines.append(l)
        x2,y2=adjust(port,x2,y2)
        #创建并启动新交换机
        new_sw=SwitchNode(x2,y2,100,50,self.swCount,port,QPushButton(self),QTextEdit(self))
        self.swCount+=1
        new_sw.switch.work()
        #将新交换连接到目标交换机上，并启动两个连接端口
        link_sw.add_activePort(port)
        new_sw.add_activePort((port+2)%4)
        p1=link_sw.getport(port)
        p2=new_sw.getport((port+2)%4)
        p1.link2port(p2.port)
        p2.link2port(p1.port)
        start(p1.work)
        start(p2.work)
        #将机器节点添加到列表中
        self.switches.append(new_sw)
        new_sw.show()
        self.update()

    def initSwitch(self):
        self.swCount=0
        swnode=SwitchNode(650,370,100,50,self.swCount,-1,QPushButton(self),QTextEdit(self))
        self.swCount += 1
        swnode.switch.work()
        #初始化一个交换机并将其加入列表
        self.switches.append(swnode)
        swnode.show()
        self.update()


if __name__ == '__main__':
    random.seed(a=None, version=2)
    app = QApplication(sys.argv)
    test = Main()
    test.show()
    sys.exit(app.exec_())