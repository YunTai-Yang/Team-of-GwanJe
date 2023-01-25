import struct
import serial
import numpy as np

class Receiver:
    def __init__(self):
        self.ser = serial.Serial(port='COM4',
                    baudrate = 9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_TWO,
                    bytesize=serial.EIGHTBITS,
                    timeout=2)

    def run(self):
        while True:
            header = self.ser.read(1)
            if header == b'?': #header
                data = header + self.ser.read(55)
                decodeData = struct.unpack('>14f', data)
                if abs(sum(decodeData[:-1])-decodeData[-1])<1:
                    alldata = np.around(decodeData[:-1],4)
                    alldata = alldata[1:]
                    print(alldata)

if __name__=="__main__":
    reciver = Receiver()
    reciver.run()