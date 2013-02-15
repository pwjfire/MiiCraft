import serial
from serial.serialutil import SerialException

import _winreg as winreg
import itertools

def enumerate_serial_ports():
    """ Uses the Win32 registry to return an
        iterator of serial (COM) ports
        existing on this computer.
    """
    path = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
    except WindowsError:
        # raise IterationError
        raise EnvironmentError 

    for i in itertools.count():
        try:
            val = winreg.EnumValue(key, i)
            yield str(val[1])
        except EnvironmentError:
            break

import re


def full_port_name(portname):
    """ Given a port-name (of the form COM7,
        COM12, CNCA0, etc.) returns a full
        name suitable for opening with the
        Serial class.
    """
    m = re.match('^COM(\d+)$', portname)
    if m and int(m.group(1)) < 10:
        return portname
    return '\\\\.\\' + portname    

def tryopen(ports):
        for i in ports:
            #fullname = full_port_name(str(cur_item.text()))
            try:
                ser = serial.Serial(i, 38400)
                ser.close()
                print i, " Open sucessfully!"
            except SerialException, e:
                print i, " Failed to Open!"
              
