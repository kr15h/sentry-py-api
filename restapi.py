#!/usr/bin/env python
import serial
import time
from datetime import datetime
import sentry
import web

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
    quit()

# Setup web server
urls = (
    #  Translates to /a1/on or /a1/off
    '/(.+)/(.+)', 'switch'  
)

app = web.application(urls, globals())
numRetryAttempts = 3

class switch:
    def GET(self, switchId, switchState):
        output = '' 
        global numRetryAttempts
        numRetryAttempts = 3
        if connect(ser):
            if switchState.lower() == 'on':
                sentrySwitchState = sentry.SwitchState.ON
            else:
                sentrySwitchState = sentry.SwitchState.OFF
            if sentry.switch(ser, switchId.lower(), sentrySwitchState):
                output = 'Successfuly changed state of ' + switchId + ' to ' + switchState  
            else:
                raise web.internalerror('Failed')
        else:
            return web.internalerror('Failed') 
        return output 

def connect(serialObject):
    serialStatus = sentry.getSerialStatus(serialObject)
    if serialStatus == sentry.Status.LOGGED_OUT:
        if not sentry.loginWithPassword(ser, 'admn'):
            print 'Login failed' 
            return False
        else:
            print 'Login success' 
            return True
    elif serialStatus == sentry.Status.LOGGED_IN:
        print 'Already logged' 
        return True
    else:
        global numRetryAttempts
        if numRetryAttempts > 0:
            numRetryAttempts = numRetryAttempts - 1
            time.sleep(1)
            return connect(serialObject)
        else:
            return False
            print 'Unknown serial device status'

if __name__ == "__main__":
    app.run()

import atexit
atexit.register(ser.close)
