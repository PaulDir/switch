import queue
from time import time
from threading import Timer

# 参数
max_entry_num = 4
max_port_num = 4
max_age = 10
check_interval = 1


class DMA:
    class Entry:
        def __init__(self):
            self.present: bool = False
            self.mac_addr: str = '0x000000000000'
            self.port: int = 0
            self.timestamp: float = 0
        def set_value(self, present, mac_addr, port, timestamp):
            self.present = present
            self.mac_addr = mac_addr
            self.port = port
            self.timestamp = timestamp

        def streamline(self):
            return '{:d}\t{}\t{}\t{:f}\t\n' \
                .format(self.present, self.mac_addr, self.port, self.timestamp)

    class AgingChecker(Timer):
        def run(self):
            while not self.finished.is_set():
                self.function(*self.args, **self.kwargs)
                self.finished.wait(check_interval)

    def __init__(self,window):
        self.window = window
        self.table = []
        self.timer = self.AgingChecker(check_interval, self.__check__)
        for i in range(max_entry_num):
            self.table.append(self.Entry())
        self.__sync__()
        self.timer.start()

    def __sync__(self):
        with open('mac_addr_t.tab', 'w') as file:
            file.writelines(list(map(lambda e: e.streamline(), self.table)))

    def __check__(self):
        for i in range(max_entry_num):
            if self.table[i].present and self.table[i].timestamp > max_age:
                self.table[i].set_value(False, 0, 0, 0)
                self.window.updateTableItem(i,self.table[i])
        self.__sync__()

    def __stop__(self):
        self.timer.cancel()

    # 接口1
    def add(self, mac_addr: str, port) -> None:
        for i in range(max_entry_num):
            if self.table[i].present and self.table[i].mac_addr == mac_addr:
                #print('已存在地址为', mac_addr, '的项')
                self.table[i].timestamp = 0
                self.table[i].port = port
                self.window.updateTableItem(i, self.table[i])
                self.__sync__()
                return
        #print('需要添加一项', mac_addr, port)
        for i in range(max_entry_num):
            if not self.table[i].present:
                #print('  有空槽')
                self.table[i].set_value(True, mac_addr, port, 0)
                self.window.updateTableItem(i, self.table[i])
                self.__sync__()
                return
        j = 0
        for i in range(max_entry_num):
            if self.table[i].timestamp < self.table[j].timestamp:
                j = i
        #print('  已满 需要替换掉第', j, '项')
        self.table[j].set_value(True, mac_addr, port, 0)
        self.window.updateTableItem(j, self.table[j])
        self.__sync__()

    # 接口2
    def query(self, mac_addr: str) :
        index=-1
        for i in range(max_entry_num):
            if self.table[i].present and self.table[i].mac_addr == mac_addr:
                #print('查询成功')
                self.table[i].timestamp=0
                self.window.updateTableItem(i, self.table[i])
                index=i
                return self.table[i].port

        for i in range(max_entry_num):
            self.table[i].timestamp+=1
        self.window.updateAge()
        #print('查询失败')
        return -1
