#!/usr/bin/env python

## P14219 - MARSUPIAL
## Authors: Nicolas Gallardo & Jared Raby
## This program will package and send the proper serial commands to the AMC motor controllers according to the incoming velocity values from the Xbox contoller 


import rospy
import math
import binascii
import serial
import struct
import string
import crc16
from std_msgs.msg import Float32

motor_max = 4000.0
count_rev = 16384.0

gain_access = "\xA5\x3F\x02\x07\x00\x01\xB3\xE7\x0F\x00\x10\x3E"
enable_bridge = "\xA5\x3F\x02\x01\x00\x01\x01\x47\x00\x00\x00\x00"
vel_mode = "\xA5\x3F\x02\x45\x00\x02"

motor_com_1 = serial.Serial(
	port='/dev/ttyS0',
	baudrate=115200, 
	parity=serial.PARITY_NONE,
	stopbits=serial.STOPBITS_ONE,
	bytesize=serial.EIGHTBITS
)

motor_com_2 = serial.Serial(
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
	
	print 'COM0 is open!'

	#Gain write-access to motor controllers
	motor_com_1.write(gain_access)

	#Enable Bridge
	motor_com_1.write(enable_bridge)


if motor_com_2.isOpen()==True:

	print 'COM1 is open!'

	#Gain write-access to motor controllers
	motor_com_2.write(gain_access)

	#Gain write-access to motor controllers
	motor_com_2.write(enable_bridge)

def motormath(vscale):
	
	rpm_val = motor_max * vscale
	mc_conv = (rpm_val * count_rev) / 60.0
	raw_vel = mc_conv * (6.5536)
	mc_final = int(raw_vel)
	return mc_final

def checksum_calc(velocity):

	cksum = crc16.crc16xmodem(velocity)
	return(cksum)

def callbackmotor1(data):

	vel_1 = motormath(data.data)

	if vel_1 < 0: 
		vel_1_hex = hex((abs(vel_1) ^ 0xffffffff) +1)[2:].strip( 'L' )
	else:
		vel_1_hex = hex(vel_1)[2:].zfill(8)

	vel_1_hex_int = int(vel_1_hex,16)

	# Converts the velocity hex value into the little endien format and puts it into the
	# proper hex format and gets the CRC value
	vel_1_final = struct.pack('<q', vel_1_hex_int).encode('hex')[:8]

        chk_sum_data = hex(crc16.crc16xmodem(binascii.a2b_hex(vel_1_final))).strip('0x').zfill(4)
 		
	# Generates the word number value and calculates the CRC
	#cmd_word_count = "{0:0>2}".format(hex(int(math.floor(len(vel_1_final.rstrip('0'))/2))).strip( '0x' ))
	cmd_word_count = struct.pack('h', int(math.floor(len(vel_1_final.rstrip('0'))/2))).encode('hex')[:2]

	chk_sum_cmd = hex(crc16.crc16xmodem(vel_mode + binascii.a2b_hex(cmd_word_count))).strip('0x')	
	
	motor_command_1 = binascii.b2a_hex(vel_mode) + chk_sum_cmd + vel_1_final + chk_sum_data

	print "Motor 1 Command:"	
	print motor_command_1

def callbackmotor2(data):
   
	vel_2 = motormath(data.data)

	if vel_2 < 0: 
		vel_2_hex = hex((abs(vel_2) ^ 0xffffffff) +1)[2:].strip( 'L' )
	else:
		vel_2_hex = hex(vel_2)[2:].zfill(8)

	vel_2_hex_int = int(vel_2_hex,16)

	# Converts the velocity hex value into the little endien format and puts it into the
	# proper hex format and gets the CRC value
	vel_2_final = struct.pack('<q', vel_2_hex_int).encode('hex')[:8]

        chk_sum_data = hex(crc16.crc16xmodem(binascii.a2b_hex(vel_2_final))).strip('0x').zfill(4)
 		
	# Generates the word number value and calculates the CRC
	#cmd_word_count = "{0:0>2}".format(hex(int(math.floor(len(vel_1_final.rstrip('0'))/2))).strip( '0x' ))
	cmd_word_count = struct.pack('h', int(math.floor(len(vel_2_final.rstrip('0'))/2))).encode('hex')[:2]

	chk_sum_cmd = hex(crc16.crc16xmodem(vel_mode + binascii.a2b_hex(cmd_word_count))).strip('0x')	
	
	motor_command_2 = binascii.b2a_hex(vel_mode) + chk_sum_cmd + vel_2_final + chk_sum_data
	
	print "Motor 2 Command:"
	print motor_command_2

def motor():

	sub1 = rospy.Subscriber("vel_1_float", Float32, callbackmotor1)
	sub2 = rospy.Subscriber("vel_2_float", Float32, callbackmotor2)


if __name__ == '__main__':

	rospy.init_node('motor_control', anonymous=True)

	motor()

	try:
		print "try"	
		while not rospy.is_shutdown():
			print "try, try again"	
			rospy.spin()
			#r.sleep()

	except rospy.ROSInterruptException: pass

#!/usr/bin/env python
