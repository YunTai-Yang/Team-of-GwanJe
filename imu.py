import time
import numpy as np
import serial
import struct
from datetime import datetime


class ImuRead:
    def __init__(self):
        self.ser_imu = serial.Serial(port='COM7',
                         baudrate=921600)


        self.ser_rf =serial.Serial(port='COM6',
                    baudrate = 115200,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_TWO,
                    bytesize=serial.EIGHTBITS,
                    timeout=0.1)

        self.header_pass = 0
        self.index = 0
        self.raw_imu = np.zeros(66)
        self.raw_imu = self.raw_imu.astype(int)
        self.status = np.zeros(13)

        self.num = 0
        self.sum = 0

        self.header = b'A'+b'B'
        self.n=0



    def run(self):
        t1 = time.time()
        while True:
            data = self.ser_imu.read()[0]
            # print(data)
            if data == 85 and self.header_pass == 0 and self.index == 0:
                self.raw_imu[self.index] = data
                self.index = 1

            elif data == 81 and self.header_pass == 0 and self.index == 1:
                
                self.raw_imu[self.index] = data
                self.index = 2
                self.header_pass = 1

            elif self.header_pass == 1 and self.index < 66:

                self.raw_imu[self.index] = data
                self.index += 1

            elif self.header_pass == 1 and self.index >= 66:
                
                # Decode and send datas
                self.decode_raw()

                # Reset index
                self.header_pass = 0
                self.index = 0
                
                # Set update rate
                self.num += 1
                dt = time.time()-t1
                self.sum += dt
                # print('Average Update rate : %.2f Hz'%(self.num/self.sum))
                t1 = time.time()


    def decode_raw(self):
        ax = self.cal16((self.raw_imu[3] << 8 | self.raw_imu[2]))/32768*16
        ay = self.cal16((self.raw_imu[5] << 8 | self.raw_imu[4]))/32768*16
        az = self.cal16((self.raw_imu[7] << 8 | self.raw_imu[6]))/32768*16

        wx = self.cal16(self.raw_imu[14] << 8 | self.raw_imu[13])/32768*2000
        wy = self.cal16(self.raw_imu[16] << 8 | self.raw_imu[15])/32768*2000
        wz = self.cal16(self.raw_imu[18] << 8 | self.raw_imu[17])/32768*2000

        roll  = self.cal16(self.raw_imu[25] << 8 | self.raw_imu[24])/32768*180
        pitch = self.cal16(self.raw_imu[27] << 8 | self.raw_imu[26])/32768*180
        yaw   = self.cal16(self.raw_imu[29] << 8 | self.raw_imu[28])/32768*180
        # mag 33 ~ 43

        temp = self.cal16(self.raw_imu[9] << 8 | self.raw_imu[8])/100

        pressure = (self.raw_imu[38] << 24| self.raw_imu[37] << 16| self.raw_imu[36] << 8 | self.raw_imu[35])/100000
        height   = (self.raw_imu[42] << 24| self.raw_imu[41] << 16| self.raw_imu[40] << 8 | self.raw_imu[39])/100

        longitude = (self.raw_imu[49] << 24 | self.raw_imu[48] << 16 | self.raw_imu[47] << 8 | self.raw_imu[46])
        latitude  = (self.raw_imu[53] << 24 | self.raw_imu[52] << 16 | self.raw_imu[51] << 8 | self.raw_imu[50])

        speed = (self.raw_imu[64] << 24 | self.raw_imu[63] << 16 | self.raw_imu[62] << 8 | self.raw_imu[61])/1000*3.6
        longitude = longitude//10000000 + (longitude%10000000/6000000)
        latitude  = latitude//10000000 + (latitude%10000000/6000000)



        now = datetime.now()
        time_string = now.strftime("%H:%M:%S.%f")[:-4]
        strt_list = [now.strftime("%H"), now.strftime("%M"), now.strftime("%S"), now.strftime("%f")[:-4]]
        time_list = np.array(list(map(float, strt_list)))

        self.status = np.array([roll,pitch,yaw,wx,wy,wz,ax,ay,az,latitude,longitude,height,speed])
        checksum = np.sum(self.status)
        packet = np.hstack((time_list,self.status,checksum))
        
        packed_bytes = self.header+struct.pack('>{}f'.format(len(packet)), *packet)
        
        self.ser_rf.write(packed_bytes)
        self.n+=1
        # print(speed)
        # time.sleep(0.01)




    def cal16(self,data):
        if data > 32768:
            return data - 65536
        else:
            return data

    def cal32(self,data):
        if data > 2**31:
            return data - 2**32
        else:
            return data
        



if __name__ == '__main__':
    imu = ImuRead()
    imu.run()