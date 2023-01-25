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
            if header1 == b'?\x80\x00\x00':
                header2 = self.ser.read(4)
                if header2 == b'@\x00\x00\x00':
                    time = self.ser.read(16)
                    decodetime = struct.unpack('>4f', time)
                    time_list = tuple(np.around(np.array(decodetime, dtype=float),1))
                    data = self.ser.read(52)
                    decode_data = struct.unpack('>13f', data)
                    if abs(sum(decode_data[:-1])-decode_data[-1])<1:
                        processed_data = np.around(decode_data[:-1],4)
                        alldata = np.concatenate((time_list, processed_data),axis=0)
                        print(alldata)
                        self.datahub.update(alldata)
    
if __name__=="__main__":
    reciver = Receiver(Datahub())
    reciver.start()