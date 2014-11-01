#!/usr/bin/env python
## Simple talker demo that listens to std_msgs/Strings published 
## to the 'chatter' topic

import rospy
import math
import binascii
import serial
import struct
#import crc16
from std_msgs.msg import Float32

motor_max = 2000.0
count_rev = 16384.0

gain_access_dirty = "\xA5\x3F\x02\x07\x00\x01\xB3\xE7\x0F\x00\x10\x3E"
enable_bridge_dirty = "\xA5\x3F\x02\x01\x00\x01\x01\x47\x00\x00\x00\x00"
gofast = "\xA5\x3F\x02\x45\x00\x02\xF0\x49\x55\x55\x01\x00\x4F\x71"

#set up serial port

motor_com_1 = serial.Serial(
	port='/dev/ttyS0',
	baudrate=115200, 
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)

#close and re-open for shits and gigs

#motor_com_1.close()
#motor_com_1.open()
if motor_com_1.isOpen()==True:
	
	print 'COM is open!'

	#Gain write-access to motor controllers

	motor_com_1.write(gain_access_dirty)

	print 'Write access granted!'

	#Enable Bridge

	motor_com_1.write(enable_bridge_dirty)

	print 'Bridge Enabled!'

	motor_com_1.write(gofast)
else:
	print 'error opening COM port'

def motormath(vscale):
	
	rpm_val = motor_max * vscale
	mc_conv = (rpm_val * count_rev) / 60.0
	raw_vel = mc_conv * (6.5536)
	mc_final = int(raw_vel)
	return mc_final

#def checksum_calc(velocity)

#	cksum = print(crc16.crc16xmodem(velocity))
#	return(cksum)

#def callbackmotor1(data):
#
#	vel_1 = motormath(data.data)
#
#	# Transform vel 1 to little endien respresentation
#	vel_1_endien = vel_1 transformed
#
#	# This is where the velcity data will be parsed. The number of words will be parsed out of it
#	# 	#bytes = odd -> l = (#bytes - 1)/2
#	#	#bytes = even -> l = #bytes/2
#	
#	chk_sum_wordcount = #fill in here
#	chk_sum_1 = command_p1 + ch_sum_wordcount
#
#	chk_sum_header = checksum_calc(check_sum_1)
#	chk_sum_data = checksum_calc(vel_1_endien)
#
#	motor_1_final = chk_sum_p1 + ck_sum_header + vel_1_endien + chk_sum_data
#
#	motor_com_1.write('motor_1_final')
		
#def callbackmotor2(data):
 #   
#	vel_2 = motormath(data.data)
#
#	# Transform vel 1 to little endien respresentation
#	vel_2_endien = vel_2 transformed
#
#	# This is where the velcity data will be parsed. The number of words will be parsed out of it
#	# 	#bytes = odd -> l = (#bytes - 1)/2
#	#	#bytes = even -> l = #bytes/2
#	
#	chk_sum_wordcount = #fill in here
#	chk_sum_1 = command_p1 + ch_sum_wordcount
#
#	chk_sum_header = checksum_calc(check_sum_1)
#	chk_sum_data = checksum_calc(vel_1_endien)
#
#	motor_2_final = chk_sum_p1 + ck_sum_header + vel_1_endien + chk_sum_data
#
#	motor_com_1.write('motor_2_final')

#def motor():

#	sub1 = rospy.Subscriber("vel_1_float", Float32, callbackmotor1)
#	sub2 = rospy.Subscriber("vel_2_float", Float32, callbackmotor2)

#if __name__ == '__main__':
#
#	rospy.init_node('motor_control', anonymous=True)
#	r = rospy.Rate(10)
#	motor()
#
#	try:
#	
#		while not rospy.is_shutdown():
#			
#			rospy.spin()
#			r.sleep()
#
#	except rospy.ROSInterruptException: pass
