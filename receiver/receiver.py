from struct import unpack
from serial import Serial, PARITY_NONE, STOPBITS_TWO, EIGHTBITS
from numpy import sum, around
from threading import Thread
from time import sleep
#from datahub import Datahub

class Receiver(Thread):
    def __init__(self, datahub):
        super().__init__()
        self.datahub = datahub
        self.first_time = True
        self.ser = None


    def setSerial(self,myport,mybaudrate):
            self.ser = Serial(port=myport,
                                    baudrate = mybaudrate,
                                    parity=PARITY_NONE,
                                    stopbits=STOPBITS_TWO,
                                    bytesize=EIGHTBITS,
                                    timeout=0.1)

    def _decode_data(self, data_bytes):
        decode_data = unpack('<18f', data_bytes)
        print(decode_data)

        if sum(decode_data[4:-1])-decode_data[-1]<1:
            all_data = around(decode_data,4)
            if len(all_data)>=1:
                self.datahub.update(all_data)


    def run(self):
        while True:
            try:
                if self.datahub.iscommunication_start:
                    if self.first_time:
                        self.setSerial(self.datahub.mySerialPort,self.datahub.myBaudrate)
                        self.first_time=False

                    if not self.ser.is_open:
                        self.ser.open()

                    self.datahub.serial_port_error=0
                    header1 = self.ser.read(1)

                    if header1 == b'A':
                        header2 = self.ser.read(1)

                        if header2 == b'B':
                            bytes_data = self.ser.read(72)
                            self._decode_data(bytes_data)
                    sleep(0.001)

                else:
                    if self.ser != None and self.ser.is_open :
                        self.ser.close()
                    sleep(0.05)
            except:
                self.datahub.serial_port_error=1


if __name__=="__main__":
    receiver = Receiver()
    receiver.run()