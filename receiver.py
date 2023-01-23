import struct
import serial
import numpy as np

class Receiver:
    def __init__(self):
        self.ser = serial.Serial(port='COM3',
                    baudrate = 9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_TWO,
                    bytesize=serial.EIGHTBITS,
                    timeout=2)

    def run(self):
        while True:
            str = self.ser.read(1)
            if str == b'A': #header
                data = str+self.ser.read(51)
                decodeData = struct.unpack('>13f', data)
                if abs(sum(decodeData[:-1])-decodeData[-1])<1:
                    alldata = np.around(decodeData[:-1],4)
                    print(alldata)

if __name__=="__main__":
    reciver = Receiver()
    reciver.run()