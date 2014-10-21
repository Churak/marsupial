#include "ros/ros.h"
#include "geometry_msgs/Twist.h"
#include "sensor_msgs/Joy.h"

#define AXIS_SPD 1
#define AXIS_TURN 0

#define SPEED_SCALE 2.0
#define TURN_SCALE 1.0

ros::Publisher pub;
ros::Subscriber sub;

geometry_msgs::Twist robotSpd;

void joyCallback(const sensor_msgs::Joy::ConstPtr& joy) {
    if( joy->buttons[1] )
    {
        robotSpd.linear.x = 0.0;
        robotSpd.angular.z = 0.0;
    }
    else
    {
        robotSpd.linear.x = SPEED_SCALE * joy->axes[AXIS_SPD];
        robotSpd.angular.z = TURN_SCALE * joy->axes[AXIS_TURN];
    }

    pub.publish(robotSpd);
}

int main(int argc, char** argv) {
	ros::init(argc, argv, "joy2drive");

	ros::NodeHandle n;

	pub = n.advertise<geometry_msgs::Twist>("/amosbase/amos_set_speed", 1);
	sub = n.subscribe<sensor_msgs::Joy>("joy", 1, joyCallback);

    ros::spin();

}
