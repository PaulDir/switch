import struct
import sys


base=60000
def replace(mac):
    m = mac[2:]  # 去掉0x

    mac_str = ''
    for i in range(len(m)):
        temp = bin(int(m[i], 16))[2:]

        if len(temp) < 4:
            temp = (4 - len(temp)) * '0' + temp
        mac_str += temp

    return mac_str


# 将数据部分变成二进制字符串形式
def str2bin(data_be):
    data = ''
    for i in range(len(data_be)):
        temp = bin(ord(data_be[i]))[2:]
        if len(temp) < 8:
            temp = (8 - len(temp)) * '0' + temp
        data += temp
    return data


# 长度变为二进制字符串形式
def len2bin(data):
    temp = bin(len(data))[2:]
    if len(data) > 1500:
        print
        sys.stderr, "数据部分超过1500个字节"
        return False
    if len(temp) < 16:
        temp = (16 - len(temp)) * '0' + temp
    return temp


# FCS算法
def FCS(mac1, mac2, data):
    a = replace(mac1) + replace(mac2) + \
        len2bin(data) + str2bin(data) + 32 * '0'
    temp = int(a[:9], 2)
    i = 9
    while i <= len(a):
        if temp < 256:
            num = 0
        else:
            num = 263
        temp = int(bin(temp ^ num)[2:] + a[i:i + 1], 2)
        i += 1
    return bin(temp)[2:]


# 补齐ADR为10位

def adr_padding(adr):
    if len(adr) < 14:
        return adr[0:2] + (14 - len(adr)) * '0' + adr[2:]
    else:
        return adr


# 补齐FTYPE为10位
def ftype_padding(ftype):
    if len(ftype) < 6:
        return ftype[0:2] + (10 - len(ftype)) * '0' + ftype[2:]
    else:
        return ftype


# 补齐FCS为10位
def fcs_padding(fcs):
    if len(fcs) < 10:
        return fcs[0:2] + (10 - len(fcs)) * '0' + fcs[2:]
    else:
        return fcs


class Forwarder(object):
    def __init__(self,DMA,n):
        self.DMA=DMA
        self.n=n
    def forward(self, package, src_port):
        src_adr, dst_adr, ftype, fcs, data = self.decode(package)
        # print(src_adr)
        # print(src_port)
        self.DMA.add(src_adr, src_port)
        if self.filter(src_adr, dst_adr) is not True:
            return []
        dst_ports = []
        flag = 0  # flag=0-单播，且找到地址；flag=1组播/广播/未在MAC地址表中找到地址
        if dst_adr == '0xffffffffffff' or dst_adr[3] in {'1', '3', '5', '7', '9', 'b', 'd', 'f'}:
            flag = 1  # 广播或组播
        if flag == 0:
            pt = self.DMA.query(dst_adr)
            print(type(pt))
            if pt !=-1:
                dst_ports.append(pt-base-4*self.n-1)
            else:
                flag = 1
        if flag == 1:
            for i in range(4):  # port_table是全局变量，记录了所有端口号
                if base+4*self.n+i+1 != src_port:
                    dst_ports.append(i)

        return dst_ports

    def decode(self, package):
        a, b, c, d, e = struct.unpack(
            '12s12s4s8s' + str(len(package) - 36) + 's', package)
        src_adr = a.decode('utf-8')
        dst_adr = b.decode('utf-8')
        ftype = c.decode('utf-8')
        fcs = d.decode('utf-8')
        data=e
        return src_adr, dst_adr, ftype, fcs, data

    def filter(self, src_adr, dst_adr):
        if src_adr == dst_adr:
            return False  # check的结果决定了frameforwarder是否转发帧
        else:
            return True