import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
ser = serial.Serial(
    port='COM3',
    baudrate=9600,
    parity=serial.PARITY_ODD,
    stopbits=serial.STOPBITS_TWO,
    bytesize=serial.SEVENBITS
)

ser.isOpen()

# send some data
ser.write(b'Hello, RF World!')
print("Data sent!")

# read data coming from the RF device
while True:
    data = ser.readline()
    print(data)

ser.close()
