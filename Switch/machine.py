import re
import socket
import struct
import zlib
import queue
from threading import Thread

IP = '127.0.0.1'
bufsize = 1526

def fcs_padding(fcs):
    if len(fcs) < 8:
        return  (8 - len(fcs)) * '0' + fcs
    else:
        return fcs


def package(src_mac,des_mac,ftype,data):
    crc = zlib.crc32(data)
    fcs = hex(crc)[2:]
    fcs = fcs_padding(fcs)
    return struct.pack('12s12s4s8s' + str(len(data)) + 's',
                    src_mac.encode('utf-8'), des_mac.encode('utf-8'), ftype.encode('utf-8'), fcs.encode('utf-8'),
                     data)

def extend_mac(mac):
    res=''
    for i in range(0,10,2):
        res+=mac[i:i+2]+':'
    return res+mac[10:12]

class Machine:
    def __init__(self,mac,window):
        self.window=window
        self.mac_str=mac
        self.mac=''.join(re.split('[:-]', mac))
        self.skt=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def send(self, dest_mac, data):
        dest_str=dest_mac
        dest_mac=''.join(re.split('[:-]', dest_mac))
        if dest_mac == 'ffffffffffff':
            self.window.addmsg("广播" + str(len(data)) + "字节数据\n\n")
        elif dest_mac[1] in {'1', '3', '5', '7', '9', 'b', 'd', 'f'}:
            self.window.addmsg("组播" + str(len(data)) + "字节数据\n\n")
        else:
            self.window.addmsg("发送"+str(len(data))+"字节数据到"+dest_str+"\n\n")

        datalen=len(data)
        if datalen<1500:
            frame = package(self.mac, dest_mac, '0800', data)
            self.skt.send(frame)
        else:
            while datalen>1500:
                send_dt=data[:1500]
                data=data[1500:]
                datalen-=len(send_dt)
                frame=package(self.mac,dest_mac,'0800',send_dt)
                self.skt.send(frame)

    def receive(self):
        frame=self.skt.recv(bufsize)
        src_adr, dst_adr, ftype, fcs, data= struct.unpack(
            '12s12s4s8s' + str(len(frame) - 36) + 's', frame)
        src_adr = src_adr.decode('utf-8')
        dst_adr = dst_adr.decode('utf-8')

        if dst_adr==self.mac or dst_adr=='ffffffffffff' or dst_adr[1] in {'1', '3', '5', '7', '9', 'b', 'd', 'f'}:
            self.window.addmsg("从"+extend_mac(src_adr)+"接收"+str(len(data))+\
                          "字节数据\n\n"+"发送响应\n\n")
            frame=self.getARP()
            self.skt.send(frame)

    def link2port(self,port):
        self.skt=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.skt.connect((IP,port))

    def work(self):
        while True:
            tr=Thread(target=self.receive)
            tr.start()

    def getARP(self):
        src_mac=self.mac
        dest_mac='xxxxxxxxxxxx'
        ftype='0806'
        data=46*b'0'
        return package(src_mac,dest_mac,ftype,data)