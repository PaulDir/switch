from switch.port import*
from switch.Forwarder import*
from switch.DMA import *
base =60000
class Switch:
    def __init__(self,n,transmitCtrl,window):
        self.window=window
        self.transmitCtrl=transmitCtrl
        self.printTransmitCtrl()
        self.dma = DMA(window)
        self.forwarder = Forwarder(self.dma,n)
        self.ports=[]
        self.active_ports=''
        self.messages=queue.Queue()
        for i in range(4):
            p=Port(i,base+4*n+i+1,transmitCtrl,self.forwarder,window)
            self.ports.append(p)

    def printTransmitCtrl(self):
        if self.transmitCtrl==0:
            self.window.ui.transmitCtrl.setText("转发方式：直通")
        elif self.transmitCtrl==1:
            self.window.ui.transmitCtrl.setText("转发方式：碎片隔离")
        elif self.transmitCtrl==2:
            self.window.ui.transmitCtrl.setText("转发方式：存储转发")
    def forward(self):
        while True:
            for i in range(4):
                while not self.ports[i].receive_frames.empty():
                    frame=self.ports[i].receive_frames.get()
                    dst_ports=self.forwarder.forward(frame,self.ports[i].port)
                    for p in dst_ports:
                        self.ports[p].send_frames.put(frame)

    def work(self):
        tf = threading.Thread(target=self.forward)
        tf.start()

    def getPort(self,n):
        return self.ports[n].port

    def getTableChange(self):
        if self.dma.changed():
            return self.dma.messages.get()
        else:
            return -1

    def getTableItem(self,i):
        return self.dma.table[i]

    def add_active_port(self,i):
        if self.active_ports=='':
            self.active_ports=str(i)
        else:
            self.active_ports+=', '+str(i)
        self.window.ui.active_port.setText("活跃端口："+self.active_ports)