import struct
import serial
import numpy as np
import threading

class Receiver(threading.Thread):
    def __init__(self, myport, datahub):
        super().__init__()
        self.ser = serial.Serial(port=myport,
                    baudrate = 9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_TWO,
                    bytesize=serial.EIGHTBITS,
                    timeout=2)
        self.count = 0
        self.datahub = datahub
        self.stop_flag = threading.Event()

    def _decode_data(self, time_bytes, data_bytes):
        time = struct.unpack('>4f', time_bytes)
        decodetime = tuple(np.around(np.array(time, dtype=float),1))
        decode_data = struct.unpack('>13f', data_bytes)
        if abs(sum(decode_data[:-1])-decode_data[-1])<1:
            angular_data = np.around(decode_data[:12],2)
            tude_data = np.around(decode_data[9:12],4)
            processed_data = np.concatenate((angular_data, tude_data),axis=0)
            alldata = np.concatenate((decodetime, processed_data),axis=0)
            return alldata

    def run(self):
        while not self.stop_flag.is_set():
            header1 = self.ser.read(4)
            if header1 == b'?\x80\x00\x00':
                header2 = self.ser.read(4)
                if header2 == b'@\x00\x00\x00':
                    time_bytes = self.ser.read(16)
                    data_bytes = self.ser.read(52)
                    data = self._decode_data(time_bytes, data_bytes)
                    if data is not None:
                        self.datahub.update(data)
                    else:
                        pass
    
    def stop(self):
        self.stop_flag.set()

if __name__=="__main__":
    receiver = Receiver()
    receiver.run()