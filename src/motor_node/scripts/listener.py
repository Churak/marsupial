#!/usr/bin/env python

## P14219 - MARSUPIAL
## Authors: Nicolas Gallardo & Jared Raby
## This program will package and send the proper serial commands to the AMC motor controllers according to the incoming velocity values from the Xbox contoller 


import rospy
import math
import binascii
import serial
import struct
#import crc16
from std_msgs.msg import Float32

motor_max = 2000.0
count_rev = 16384.0

gain_access = "\xA5\x3F\x02\x07\x00\x01\xB3\xE7\x0F\x00\x10\x3E"
enable_bridge = "\xA5\x3F\x02\x01\x00\x01\x01\x47\x00\x00\x00\x00"
#gofast = "\xA5\x3F\x02\x45\x00\x02\xF0\x49\x55\x55\x01\x00\x4F\x71"
vel_mode = "\xA5\x3F\x02\x45\x00\x02"
#set up serial port

motor_com_1 = serial.Serial(
	port='/dev/ttyS0',
	baudrate=115200, 
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)

motor_com_2 = serial.Serial)
	port='/dev/ttyS1',
	baudrate=115200,
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)

#close and re-open for shits and gigs

#motor_com_1.close()
#motor_com_1.open()
if motor_com_1.isOpen()==True:
	
#	print 'COM0 is open!'

	#Gain write-access to motor controllers

	motor_com_1.write(gain_access)

#	print 'Write access granted!'

	#Enable Bridge

	motor_com_1.write(enable_bridge)

#	print 'Bridge Enabled!'

#	motor_com_1.write(gofast)
else:
#	print 'error opening COM0 port'

if motor_com_2.isOpen()==True:

#	print 'COM1 is open!'

	motor_com_2.write(gain_access)
	
	motor_com_2.write(enable_bridge)

else:
#	print 'error opening COM1 port'


def motormath(vscale):
	
	rpm_val = motor_max * vscale
	mc_conv = (rpm_val * count_rev) / 60.0
	raw_vel = mc_conv * (6.5536)
	mc_final = int(raw_vel)
	return mc_final

def checksum_calc(velocity)

	cksum = print(crc16.crc16xmodem(velocity))
	return(cksum)

def callbackmotor1(data):

	vel_1 = motormath(data.data)

	# Transform vel 1 to little endien respresentation
	vel_1_endien = struct.pack('<i', "%08X" % vel_1)

	# This is where the velcity data will be parsed. The number of words will be parsed out of it
	# 	#bytes = odd -> l = (#bytes - 1)/2
	#	#bytes = even -> l = #bytes/2
	
	data_wordcount = #fill in here
	command_header = vel_mode + data_wordcount

	chk_sum_header = checksum_calc(command_header)
	chk_sum_data = checksum_calc(vel_1_endien)

	motor_1_final = command_header + str(ck_sum_header) + str(vel_1_endien) + str(chk_sum_data)

	motor_com_1.write(motor_1_final)
	
def callbackmotor2(data):
   
	vel_2 = motormath(data.data)

	# Transform vel 1 to little endien respresentation
	vel_2_endien = struct.pack('<i', "%08X" % vel_2)

	# This is where the velcity data will be parsed. The number of words will be parsed out of it
	# 	#bytes = odd -> l = (#bytes - 1)/2
	#	#bytes = even -> l = #bytes/2
	
	data_wordcount = #fill in here
	command_header = vel_mode + data_wordcount

	chk_sum_header = checksum_calc(command_header)
	chk_sum_data = checksum_calc(vel_2_endien)

	motor_2_final = command_header + str(chk_sum_header) + str(vel_2_endien) + str(chk_sum_data)

	motor_com_2.write(motor_2_final)

def motor():

	sub1 = rospy.Subscriber("vel_1_float", Float32, callbackmotor1)
	sub2 = rospy.Subscriber("vel_2_float", Float32, callbackmotor2)

if __name__ == '__main__':

	rospy.init_node('motor_control', anonymous=True)
	r = rospy.Rate(10)
	motor()

	try:
	
		while not rospy.is_shutdown():
			
			rospy.spin()
			r.sleep()

	except rospy.ROSInterruptException: pass
