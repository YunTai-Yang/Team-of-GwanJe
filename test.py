from ctypes import *
import struct

binary_data = bytearray(48)
size1 = size2 = 4
size3 = len(binary_data) - size1 - size2

part1 = (c_char * size1).from_buffer(binary_data)
part2 = (c_char * size2).from_buffer(binary_data, size1)
part3 = (c_char * size3).from_buffer(binary_data, size1 + size2)
struct.pack_into('12F', part3, 0, 1.23, 2.14, 3.32, 4.24, 5.13, 6.14, 7.32, 189.22, 6.32, 23.0256, 15.23456, 30.67890)

print(binary_data[24:])
#bytearray(b'\x01\x00\x00\x00\x02\x00\x00\x00\x03\x00\x00\x00\x04\x00\x00\x00')

print(struct.unpack_from('12F', part3))
#(1, 2, 3, 4)