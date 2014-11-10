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

	# Represents te number in little endian notation
	vel_1_final = struct.pack('<q', vel_1_hex_int).encode('hex')[:8]
	vel_1_final_hex = "\\x" +  "\\x".join(vel_1_final[i:i+2] for i in range(0, 8, 2))

        chk_sum_data = crc16.crc16xmodem(repr(vel_1_final))
 
	#apples = ":".join("{:02x}".format(ord(c)) for c in str(motor_1_final))
	
	print vel_1_final
	print hex(chk_sum_data)
	
	
def callbackmotor2(data):
   
	vel_2 = motormath(data.data)

	vel_2_endien = vel_2
	
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
