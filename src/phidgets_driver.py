(self._interfaceKit#!/usr/bin/env python

#Basic imports
from ctypes import *
import sys
import random
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, InputChangeEventArgs, OutputChangeEventArgs, SensorChangeEventArgs
from Phidgets.Devices.InterfaceKit import InterfaceKit
from Phidgets.Phidget import PhidgetLogLevel


class Phidget(object):
    def __init__(self, sensor_change_cb=self._interfaceKitSensorChanged):
        self.interfaceKit = InterfaceKit()

        self.interfaceKit.setOnAttachHandler(self._interfaceKitAttached)
        self.interfaceKit.setOnDetachHandler(self._interfaceKitDetached)
        self.interfaceKit.setOnErrorhandler(self._interfaceKitError)
        self.interfaceKit.setOnInputChangeHandler(self._interfaceKitInputChanged)
        self.interfaceKit.setOnOutputChangeHandler(self._interfaceKitOutputChanged)
        self.interfaceKit.setOnSensorChangeHandler(self._interfaceKitSensorChanged)

    def displayDeviceInfo():
        print("|------------|----------------------------------|--------------|------------|")
        print("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
        print("|------------|----------------------------------|--------------|------------|")
        print("|- %8s -|- %30s -|- %10d -|- %8d -|" % (interfaceKit.isAttached(), interfaceKit.getDeviceName(), interfaceKit.getSerialNum(), interfaceKit.getDeviceVersion()))
        print("|------------|----------------------------------|--------------|------------|")
        print("Number of Digital Inputs: %i" % (interfaceKit.getInputCount()))
        print("Number of Digital Outputs: %i" % (interfaceKit.getOutputCount()))
        print("Number of Sensor Inputs: %i" % (interfaceKit.getSensorCount()))

    def _interfaceKitAttached(e):
        attached = e.device
        print("InterfaceKit %i Attached!" % (attached.getSerialNum()))

    def _interfaceKitDetached(e):
        detached = e.device
        print("InterfaceKit %i Detached!" % (detached.getSerialNum()))

    def _interfaceKitError(e):
        try:
            source = e.device
            print("InterfaceKit %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
        except PhidgetException as e:
            print("Phidget Exception %i: %s" % (e.code, e.details))

    def _interfaceKitInputChanged(e):
        source = e.device
        print("InterfaceKit %i: Input %i: %s" % (source.getSerialNum(), e.index, e.state))

    def _interfaceKitSensorChanged(e):
        source = e.device
        print("InterfaceKit %i: Sensor %i: %i" % (source.getSerialNum(), e.index, e.value))

    def _interfaceKitOutputChanged(e):
        source = e.device
        print("InterfaceKit %i: Output %i: %s" % (source.getSerialNum(), e.index, e.state))


#Main Program Code
try:
	#logging example, uncomment to generate a log file
    #interfaceKit.enableLogging(PhidgetLogLevel.PHIDGET_LOG_VERBOSE, "phidgetlog.log")


except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Opening phidget object....")

try:
    interfaceKit.openPhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Waiting for attach....")

try:
    interfaceKit.waitForAttach(10000)
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    try:
        interfaceKit.closePhidget()
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))
        print("Exiting....")
        exit(1)
    print("Exiting....")
    exit(1)
else:
    displayDeviceInfo()

print("Setting the data rate for each sensor index to 4ms....")
for i in range(interfaceKit.getSensorCount()):
    try:

        interfaceKit.setDataRate(i, 4)
    except PhidgetException as e:
        print("Phidget Exception %i: %s" % (e.code, e.details))

print("Press Enter to quit....")

chr = sys.stdin.read(1)

print("Closing...")

try:
    interfaceKit.closePhidget()
except PhidgetException as e:
    print("Phidget Exception %i: %s" % (e.code, e.details))
    print("Exiting....")
    exit(1)

print("Done.")
exit(0)
