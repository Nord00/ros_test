#! /usr/bin/env python
import rospy
import subprocess
import os
import sys
from std_msgs.msg import Float64;

from mavros_msgs.srv import CommandBool, CommandTOL, SetMode
from geometry_msgs.msg import PoseStamped,Pose,Vector3,Twist,TwistStamped
from std_srvs.srv import Empty
import time 
cur_pose = PoseStamped()
def pos_cb(msg):
    global cur_pose
    cur_pose = msg

mode_proxy = None
arm_proxy = None

rospy.init_node('multi', anonymous=True)

#Comm for drones
mode_proxy = rospy.ServiceProxy('mavros/set_mode', SetMode)
arm_proxy = rospy.ServiceProxy('mavros/cmd/arming', CommandBool)

print 'communication initialization complete'
try:
	data = rospy.wait_for_message('mavros/global_position/rel_alt', Float64, timeout=5)
except:
	pass


print "wait for service"
rospy.wait_for_service('mavros/set_mode')
print "got service"

rate = rospy.Rate(10)

while not rospy.is_shutdown():
	success = None
	try:
		success = mode_proxy(1,'OFFBOARD')
	except rospy.ServiceException, e:
		print ("mavros/set_mode service call failed: %s"%e)

	success = None
	rospy.wait_for_service('mavros/cmd/arming')
	try:
		success = arm_proxy(True)
	except rospy.ServiceException, e:
		print ("mavros1/set_mode service call failed: %s"%e)
