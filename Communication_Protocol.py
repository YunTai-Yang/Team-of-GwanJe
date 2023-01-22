import serial

class RFProtocol:
    def __init__(self, port, baudrate):
        self.ser = serial.Serial(port=port, baudrate=baudrate)

    def send_data(self, data, recipient_address):
        # Prepare the data packet with recipient address
        packet = recipient_address + data
        self.ser.write(packet)
        print("Data sent to recipient: ", recipient_address)

    def receive_data(self):
        while True:
            data = self.ser.readline()
            # Extract the sender address from the packet
            sender_address = data[:4]
            data = data[4:]
            print("Data received from: ", sender_address)
            print("Data: ", data)
            # Process the received data here
            # ...
            # ...

# Initialize the RF protocol
rf_protocol = RFProtocol(port='COM3', baudrate=9600)
# Send data to a recipient
rf_protocol.send_data(b'Hello, RF World!', b'1234')
# Receive data from correspondents
rf_protocol.receive_data()
