import socket
import threading
import queue
import struct
import time
import zlib
#import crcmod.predefined


IP = '127.0.0.1'

bufsize = 1526
Hosts = []  # 0:hostname,1:connection


def fcs_padding(fcs):
    if len(fcs) < 8:
        return  (8 - len(fcs)) * '0' + fcs
    else:
        return fcs

class Port(threading.Thread):
    global Hosts

    def __init__(self, num,port,transmitCtrl,forwarder,window):
        self.window=window
        threading.Thread.__init__(self)
        self.s_in = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.num=num
        self.port = port
        self.isActive=False
        self.transmitCtrl=transmitCtrl
        self.forwarder=forwarder
        self.send_frames = queue.Queue()  # 发送队列
        self.receive_frames = queue.Queue()  # 接收队列
        self.s_in.bind((IP, self.port))

        self.s_in.listen()
        self.count=0
        self.s_out = self.s_in
        self.outControl=0

        self.messages=queue.Queue()
    def crc16(self, data, fcs):
        crc = zlib.crc32(data.encode())
        fcs0 = hex(crc)[2:]
        fcs0 = fcs_padding(fcs0)
        if (fcs0 == fcs):
            return True
        else:
            return False

    def transmit(self, frame):
        print(frame)
        print(frame.decode())
        if self.transmitCtrl == 0:  # 直通
            self.receive_frames.put(frame)
            #print(1)
        elif self.transmitCtrl == 1:  # 碎片隔离
            if (len(frame) >= 64):
                self.receive_frames.put(frame)
        elif self.transmitCtrl == 2:  # 存储转发
            fcs = frame[28:36].decode()
            data = frame[36:].decode()
            if self.crc16(data, fcs):
                self.receive_frames.put(frame)

    def ReceiveFrames(self):
            if self.count==0 :
                self.conn, addr = self.s_in.accept()
            self.count+=1
            frame = self.conn.recv(bufsize)
            msg=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" 接收到长度为"+str(len(frame))+"字节的数据帧\n\n"
            self.window.addPortmsg(self.num,msg)
            self.messages.put(msg)
            if len(frame)!=0:
                self.transmit(frame)

    def SendFrames(self):
        if not self.send_frames.empty() & self.isActive:
            frame=self.send_frames.get()
            msg=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+" 发送长度为" + str(len(frame)) + "字节的数据帧\n\n"
            self.window.addPortmsg(self.num,msg)
            self.messages.put(msg)
            if self.outControl==0 :
                self.conn.send(frame)
            else:
                self.s_out.send(frame)

    def Send2(self,frame):
        self.s_out.send(frame)

    def link2machine(self):
        self.isActive = True
        self.outControl=0
        self.s_out=self.s_in

    def link2port(self, port):
        self.isActive=True
        self.outControl=1
        self.s_out = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_out.connect((IP,port))

    def work(self):
        while True:
            ts = threading.Thread(target=self.SendFrames)
            tr = threading.Thread(target=self.ReceiveFrames)
            ts.start()
            tr.start()


    def getMsg(self):
        if self.messages.qsize()==0:
            return 'null'
        else:
            return self.messages.get()