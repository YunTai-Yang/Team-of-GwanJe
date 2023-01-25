import struct
import serial
import numpy as np
import threading
from datahub import Datahub

class Receiver(threading.Thread):
    def __init__(self, datahub):
        super().__init__()

        self.ser = serial.Serial(port='COM4',
                    baudrate = 9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_TWO,
                    bytesize=serial.EIGHTBITS,
                    timeout=2)
        self.datahub = datahub

    def start(self):
        while True:
            header1 = self.ser.read(4)
            #print(header1)
            if header1 == b'?\x80\x00\x00':
                header2 = self.ser.read(4)
                if header2 == b'@\x00\x00\x00':
                    data = self.ser.read(52)
                    decodeData = struct.unpack('>13f', data)
                    if abs(sum(decodeData[:-1])-decodeData[-1])<1:
                        alldata = np.around(decodeData[:-1],4)
                        self.datahub.update(alldata)

    def start():
        pass
    
if __name__=="__main__":
    reciver = Receiver(Datahub())
    reciver.run()