import serial
import time
from datetime import datetime
import sentry

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
print 'Serial connection isOpen: ' + str(ser.isOpen())
if not ser.isOpen():
    print('Failed to open serial connection')
    quit()

startTime = datetime.now()

serialStatus = sentry.getSerialStatus(ser)

if serialStatus == sentry.Status.LOGGED_OUT:
    if sentry.loginWithPassword(ser, 'admn'):
        sentry.switch(ser, 'a2', sentry.SwitchState.ON)
        time.sleep(2)
        sentry.switch(ser, 'a2', sentry.SwitchState.OFF)
        time.sleep(2)
        sentry.logout(ser)
elif serialStatus == sentry.Status.LOGGED_IN:
    sentry.logout(ser)
else:
    print 'Unknown serial device status'

endTime = datetime.now()
deltaTime = endTime - startTime
print 'Operation took ' + str(deltaTime.total_seconds()) + ' seconds'  

# Close serial connection
print('Attempting to close serial connection...')
ser.close()
print 'Serial isOpen: ' + str(ser.isOpen())