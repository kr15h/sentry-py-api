import serial
import time
import re

# Enable enum
def enum(**named_values):
    return type('Enum', (), named_values)

# Define status enum
Status = enum(NONE=1, LOGGED_IN=2, LOGGED_OUT=3)
SwitchState = enum(ON='ON', OFF='OFF')

# Enable / disable debugging
debug = True

def readSerialAfterDelay(serialObject, delayTime):
    time.sleep(delayTime)
    out = ''
    while serialObject.inWaiting() > 0:
        out += serialObject.read(1)
    return out

def getSerialStatus(serialObject):
    ser.flush()
    time.sleep(0.1)
    ser.write('\r')
    time.sleep(0.1)
    ser.write('\r')
    out = readSerialAfterDelay(serialObject, 1)
    if debug: print out
    status = Status.NONE
    m = re.search('(Enter Password: )$', out)
    if m: 
        status = Status.LOGGED_OUT
        return status
    m = re.search('(Sentry: )$', out)
    if m:
        status = Status.LOGGED_IN
        return status 
    return status

def loginWithPassword(serialObject, password):
    if debug: print('Entering password')
    serialObject.write(password)
    serialObject.write('\r')
    out = readSerialAfterDelay(serialObject, 1)
    if debug: print(out)
    m = re.search('(Sentry: )$', out)
    if m:
        if debug: print('Login successful')
        return True
    else:
        if debug: print('Wrong password')
        return False

def logout(serialObject):
    if debug: print
    serialObject.flush()
    serialObject.write('quit\r')
    out = readSerialAfterDelay(serialObject, 1)
    m = re.search('(Session ended)', out)
    if m:
        if debug: print('Logout successful')
        return True
    else:
        if debug: print('Logout failed')
        return False

def switch(serialObject, switchId, switchState):
    if debug: print 'Switching ' + switchId + ': ' + switchState + '...' 
    if switchState == SwitchState.ON:
        serialObject.write('on .' + switchId)
    else:
        serialObject.write('off .' + switchId)
    serialObject.write('\r')
    out = readSerialAfterDelay(serialObject, 2)
    if debug: print out
    m = re.search('(1 port\(s\) turned)', out)
    if m: 
        if debug: print 'Success'
        return True
    else:
        if debug: print 'Failed' 
        return False

if debug: print('Configuring serial port')
ser = serial.Serial()
ser.baudrate = 19200
ser.bytesize = 8
ser.parity = 'N'
ser.stopbits = 1
ser.port = '/dev/ttyUSB0'
if debug: print(ser)
if debug: print('Attempting to open serial connection')
ser.open()
if debug:
    print 'Serial connection isOpen: ' + str(ser.isOpen())
if not ser.isOpen():
    print('Failed to open serial connection')
    quit()


serialStatus = getSerialStatus(ser)

if serialStatus == Status.LOGGED_OUT:
    if loginWithPassword(ser, 'admn'):
        switch(ser, 'a2', SwitchState.ON)
        time.sleep(2)
        switch(ser, 'a2', SwitchState.OFF)
        time.sleep(2)
        logout(ser)
elif serialStatus == Status.LOGGED_IN:
    logout(ser)
else:
    print 'Unknown serial device status'

# Close serial connection
if debug: print('Attempting to close serial connection...')
ser.close()
if debug: print 'Serial isOpen: ' + str(ser.isOpen())