/* puckdropper.cpp
 * John Greenslade, 2014
 * Puck dropper ROS control node
 */

#include "ros/ros.h"
#include "std_msgs/Bool.h"
#include <termios.h>
#include <stdio.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/signal.h>
#include <sys/types.h>

// Serial port stuff.
#define S_PORT "/dev/ttyPUCKDROP"
#define S_BAUD B9600

#define PUCK_COUNT 3 // Number of puck drop slots in the system. Max 8!

// Vars.
volatile int currentPuck = 1;
volatile int fd; // Serial port file descriptor.

void dropCallback(const std_msgs::Bool::ConstPtr& msg)
{
	if(msg->data) // Bool 1 = drop puck.
	{
		if( currentPuck > PUCK_COUNT )
		{
			ROS_WARN("No remaining pucks!");
		}
		else
		{
			ROS_INFO("Dropping puck...");
			char tx = '0' + currentPuck; // L33t ascii hax!
			write(fd, &tx, 1); // Send serial command.
			currentPuck++;
		}
	}
	else // Bool 0 = reset pucks.
	{
		ROS_INFO("Resetting pucks...");
		currentPuck = 1;
		char tx = 'r';
		write(fd, &tx, 1); // Send serial command.
	}
}

int main(int argc, char** argv)
{
	// Serial port init.
	fd = open(S_PORT, O_RDWR | O_NOCTTY | O_SYNC);
	if(fd < 0)
	{
		ROS_ERROR("Serial port " S_PORT " unable to be opened.");
		return 1;
	}
	struct termios tio;
	memset(&tio, 0, sizeof tio);
	if(tcgetattr (fd, &tio) != 0)
	{
		ROS_ERROR("error from tcgetattr");
		return 1;
	}
	cfsetospeed(&tio, S_BAUD);
	cfsetispeed(&tio, S_BAUD);

	tio.c_cflag = (tio.c_cflag & ~CSIZE) | CS8;     // 8-bit chars
	tio.c_iflag &= ~IGNBRK;
	tio.c_lflag = 0;
	tio.c_oflag = 0;
	tio.c_cc[VMIN] = 0;
	tio.c_cc[VTIME] = 5;
	tio.c_iflag &= ~(IXON | IXOFF | IXANY);
	tio.c_cflag |= (CLOCAL | CREAD);
	tio.c_cflag &= ~(PARENB | PARODD);
	tio.c_cflag &= ~CSTOPB;
	tio.c_cflag &= ~CRTSCTS;
	if (tcsetattr (fd, TCSANOW, &tio) != 0)
	{
		ROS_ERROR("error from tcsetattr");
		return 1;
	}
	//TEST
	//write(fd, "TEST", 4);

	// ROS init stuff.
	ros::init(argc, argv, "puckdropper");

	ros::NodeHandle n;

	// We subscribe to a single topic, drop.
	ros::Subscriber sub = n.subscribe("drop", 1, dropCallback);

	// SPIN!
	ROS_INFO("Puck dropper init complete.");
	ros::spin();

	return 0;
}
