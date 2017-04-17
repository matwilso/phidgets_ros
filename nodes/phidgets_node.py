#!/usr/bin/env python
from __future__ import division
#Basic imports
from ctypes import *
import sys
import random
#Phidget specific imports
from Phidgets.PhidgetException import PhidgetErrorCodes, PhidgetException
from Phidgets.Events.Events import AttachEventArgs, DetachEventArgs, ErrorEventArgs, InputChangeEventArgs, OutputChangeEventArgs, SensorChangeEventArgs
from Phidgets.Devices.InterfaceKit import InterfaceKit
from Phidgets.Phidget import PhidgetLogLevel
#ROS imports
import rospy



class Node(object):
    def __init__(self):
        rospy.init_node("phidgets_node", log_level=rospy.DEBUG)


        self.interfaceKit = InterfaceKit()
        self.interfaceKit.setOnSensorChangeHandler(self.sensorChangeCallback)

        self.interfaceKit.setOnAttachHandler(self.interfaceKitAttached)
        self.interfaceKit.setOnDetachHandler(self.interfaceKitDetached)
        self.interfaceKit.setOnErrorhandler(self.interfaceKitError)
        self.interfaceKit.setOnInputChangeHandler(self.interfaceKitInputChanged)
        self.interfaceKit.setOnOutputChangeHandler(self.interfaceKitOutputChanged)

        interfaceKit.openPhidget()

        interfaceKit.setDataRate(i, 16) # if greater than 8, must be multiple of 8

        rospy.loginfo("Waiting for phidgets attach....")
        interfaceKit.waitForAttach(10000)

        displayDeviceInfo()

    def __del__(self):
        interfaceKit.closePhidget()


    def run(self):
	"""Run the main ros loop"""
        rospy.loginfo("Starting phidgets node loop")
        r_time = rospy.Rate(10) #10 Hz looping

        while not rospy.is_shutdown():
            r_time.sleep()


    def displayDeviceInfo(self):
        rospy.debuginfo("|------------|----------------------------------|--------------|------------|")
        rospy.debuginfo("|- Attached -|-              Type              -|- Serial No. -|-  Version -|")
        rospy.debuginfo("|------------|----------------------------------|--------------|------------|")
        rospy.debuginfo("|- %8s -|- %30s -|- %10d -|- %8d -|" % (interfaceKit.isAttached(), interfaceKit.getDeviceName(), interfaceKit.getSerialNum(), interfaceKit.getDeviceVersion()))
        rospy.debuginfo("|------------|----------------------------------|--------------|------------|")
        rospy.debuginfo("Number of Digital Inputs: %i" % (interfaceKit.getInputCount()))
        rospy.debuginfo("Number of Digital Outputs: %i" % (interfaceKit.getOutputCount()))
        rospy.debuginfo("Number of Sensor Inputs: %i" % (interfaceKit.getSensorCount()))

    def interfaceKitAttached(self, e):
        attached = e.device
        rospy.loginfo("InterfaceKit %i Attached!" % (attached.getSerialNum()))

    def interfaceKitDetached(self, e):
        detached = e.device
        rospy.loginfo("InterfaceKit %i Detached!" % (detached.getSerialNum()))

    def interfaceKitError(self, e):
        try:
            source = e.device
            rospy.loginfo("InterfaceKit %i: Phidget Error %i: %s" % (source.getSerialNum(), e.eCode, e.description))
        except PhidgetException as e:
            rospy.loginfo("Phidget Exception %i: %s" % (e.code, e.details))

    def interfaceKitSensorChanged(self, e):
        source = e.device
        rospy.loginfo("InterfaceKit %i: Sensor %i: %i" % (source.getSerialNum(), e.index, e.value))


    def sensorChangeCallback(self):
        """Every time sensor changes, log all the sensor values"""
        arm_left_val = self.interfaceKit.getSensorValue(0)
        arm_right_val = self.interfaceKit.getSensorValue(1)
        bucket_left_val = self.interfaceKit.getSensorValue(2)
        bucket_right_val = self.interfaceKit.getSensorValue(3)
        pinion_left_val = self.interfaceKit.getSensorValue(4)
        pinion_right_val = self.interfaceKit.getSensorValue(5)

        rospy.logdebug("arm left raw value = %d", arm_left_val)
        rospy.logdebug("arm right raw value = %d", arm_right_val)
        rospy.logdebug("bucket left raw value = %d", bucket_left_val)
        rospy.logdebug("bucket right raw value = %d", bucket_right_val)
        rospy.logdebug("pinion left raw value = %d", pinion_left_val)
        rospy.logdebug("pinion right raw value = %d", pinion_right_val)






if __name__ == "__main__":
    try:
        node = Node()
        node.run()
    except rospy.ROSInterruptException:
        pass
    rospy.loginfo("Exiting phidgets node")
