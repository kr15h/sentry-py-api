import serial
import time
import re

print('Configuring serial port')
ser = serial.Serial()
ser.baudrate = 19200
ser.bytesize = 8
ser.parity = 'N'
ser.stopbits = 1
ser.port = '/dev/ttyUSB0'
print(ser)

print('Attempting to open serial connection')
ser.open()
print(ser.isOpen())

ser.flush()

# Emulate two successive return key hits
time.sleep(0.1)
ser.write('\r')
time.sleep(0.1)
ser.write('\r')

# Wait and read in response from the other party
time.sleep(1)
out = ''
while ser.inWaiting() > 0:
    out += ser.read(1)

# Debug
if out != '':
	print ">>" + out

# Check if the received output prompts to enter Password
m = re.search('(Enter Password: )$', out)

if m:
    print('Entering password')

    # If yes, enter Password
    ser.write('admn\r')
    time.sleep(1)
    out = ''
    while ser.inWaiting() > 0:
        out += ser.read(1)
    if out != '':
    	print ">>" + out


    ser.write('on .a1\r')
    time.sleep(2)
    ser.write('off .a1\r')
    time.sleep(2)
    ser.flush()

    # Quit
    ser.write('quit\r')
    time.sleep(1)
    out = ''
    while ser.inWaiting() > 0:
        out += ser.read(1)
    if out != '':
    	print ">>" + out

else:
    print('Failed to connect')

    # Quit
    ser.write('quit\r')
    time.sleep(1)
    out = ''
    while ser.inWaiting() > 0:
        out += ser.read(1)
    if out != '':
    	print ">>" + out
    # Perhaps try again then

print('Attempting to close serial connection')
ser.close()
print(ser.isOpen())
