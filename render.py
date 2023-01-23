import serial
import time
import struct

ser = serial.Serial(port='COM4',
                    baudrate = 9600,
                    parity=serial.PARITY_NONE,
                    stopbits=serial.STOPBITS_TWO,
                    bytesize=serial.EIGHTBITS,
                    timeout=0.2)


# float value to convert
# roll, pitch, yaw, rollSpeed, pitchSpeed, yawSpeed, Xaccel, Yaccel, Zaccel, 위도, 경도, 고도

float_list = [10.11, 20.22, 30.33, 100.11, 200.11, 300.11, 1.02, 0.92, 4.22, 37.4444, 137.6666, 90.85]
checksum = sum(float_list)
float_list.append(checksum)


while True:
    packed_bytes = struct.pack('>{}f'.format(len(float_list)), *float_list)
    ser.write(packed_bytes)
    print(packed_bytes)
    time.sleep(0.01)