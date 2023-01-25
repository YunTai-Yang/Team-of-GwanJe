import serial
import time
import struct
import random

ser = serial.Serial(port='COM3',
                    baudrate = 9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_TWO,
                    bytesize=serial.EIGHTBITS,
                    timeout=0.2)


# float value to convert
# header1, header2, roll, pitch, yaw, rollSpeed, pitchSpeed, yawSpeed, Xaccel, Yaccel, Zaccel, 위도, 경도, 고도 , checksum

while True:
    header_list = [1, 2]
    float_list = [10.11, 20.22, 30.33, 100.11, 200.11, 300.11, 1.02, 0.92, 4.22, 37.4444, 137.6666, 90.85]
    for i in range(len(float_list)):
        float_list[i] += random.uniform(-1, 1)
    data_list = header_list+float_list
    checksum = sum(float_list)
    data_list.append(checksum)

    packed_bytes = struct.pack('>{}f'.format(len(data_list)), *data_list)
    ser.write(packed_bytes)
    print(packed_bytes)
    time.sleep(0.01)