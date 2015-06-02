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
    serialObject.flush()
    time.sleep(0.1)
    serialObject.write('\r')
    time.sleep(0.1)
    serialObject.write('\r')
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
