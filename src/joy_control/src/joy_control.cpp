#include <ros/ros.h>
#include <geometry_msgs/Twist.h>
#include <sensor_msgs/Joy.h>
#include <std_msgs/Float32.h>
#include <visualization_msgs/Marker.h>


double vel_1, vel_2;

class VelSee
{

public:

    VelSee();

private:

    void joyCallback(const sensor_msgs::Joy::ConstPtr& joy);

    ros::NodeHandle nh_;

    int linear_, angular_;
    double l_scale_, a_scale_;
    ros::Subscriber joy_sub_;

};

VelSee::VelSee():

linear_(1),
angular_(0)
{
nh_.param("axis_linear", linear_, linear_);
nh_.param("axis_angular", angular_, angular_);
nh_.param("scale_angular", a_scale_, a_scale_);
nh_.param("scale_linear", l_scale_, l_scale_);

// Set up the joy subscrber
joy_sub_ = nh_.subscribe<sensor_msgs::Joy>("joy", 5, &VelSee::joyCallback, this);
}


// Velocity Visualize callback function for the sensor messages 
void VelSee::joyCallback(const sensor_msgs::Joy::ConstPtr& joy)
{
    geometry_msgs::Twist twist;
    twist.linear.x = joy->axes[linear_];
    twist.angular.z = joy->axes[angular_];
    
    double vel_1_calc, vel_2_calc;
    	
    // Calculate the velocity needed for each of the motors
    vel_1_calc = twist.linear.x - (twist.angular.z);
    vel_2_calc = twist.linear.x + (twist.angular.z); 

    if( (fabs(vel_1_calc)) > 1 || (fabs(vel_2_calc)) > 1)
    {
        if ((fabs(vel_1_calc)) > (fabs(vel_2_calc)))
        {
          vel_1 = (vel_1_calc / (fabs(vel_1_calc)));
          vel_2 = (vel_2_calc / (fabs(vel_1_calc)));	
        }
        else 
        {
          vel_1 = (vel_1_calc / (fabs(vel_2_calc)));
          vel_2 = (vel_2_calc / (fabs(vel_2_calc)));	
        }
    }
    else 
    {
      vel_1 = vel_1_calc;
      vel_2 = vel_2_calc;	
    }
}

// This sets up the marker. ID, frame, starting orientation, etc.
// *************************************************************
int main(int argc, char** argv)
{
ros::init(argc, argv, "marker_test");
VelSee VelSee;
ros::NodeHandle n;
ros::Rate r(100);
ros::Publisher vel_1_mark_pub = n.advertise<visualization_msgs::Marker>("velocity_1",0);
ros::Publisher vel_2_mark_pub = n.advertise<visualization_msgs::Marker>("velocity_2",0);
ros::Publisher vel_1_pub = n.advertise<std_msgs::Float32>("vel_1_float",0);
ros::Publisher vel_2_pub = n.advertise<std_msgs::Float32>("vel_2_float",0);

// Define the  and create the marker, called "marker"
visualization_msgs::Marker vel_1_mark;
visualization_msgs::Marker vel_2_mark;

// Setting up frame ID and timestamp for the marker	
vel_1_mark.header.frame_id = "/my_frame";
vel_1_mark.header.stamp = ros::Time::now();
vel_2_mark.header.frame_id = "/my_frame";
vel_2_mark.header.stamp = ros::Time::now();


// Set the namespace and id for this marker. This serves to create a unique ID
// Any marker sent with the same namespace and ID will overwrite the old one 
vel_1_mark.ns = "vel_1";
vel_2_mark.ns = "vel_2";
vel_1_mark.id = 0;
vel_2_mark.id = 1;

vel_1_mark.type = visualization_msgs::Marker::ARROW;
vel_2_mark.type = visualization_msgs::Marker::ARROW;
vel_1_mark.action = visualization_msgs::Marker::ADD;
vel_2_mark.action = visualization_msgs::Marker::ADD;

// Set the default position and orientation of the arrow for the marker
vel_1_mark.pose.position.x = 0;
vel_1_mark.pose.position.y = 1;
vel_1_mark.pose.position.z = 0;
vel_1_mark.pose.orientation.x = 0.0;
vel_1_mark.pose.orientation.y = 0.0;
vel_1_mark.pose.orientation.z = 0.0;
vel_1_mark.pose.orientation.w = 1.0;

vel_2_mark.pose.position.x = 0;
vel_2_mark.pose.position.y = -1;
vel_2_mark.pose.position.z = 0;
vel_2_mark.pose.orientation.x = 0.0;
vel_2_mark.pose.orientation.y = 0.0;
vel_2_mark.pose.orientation.z = 0.0;

// Determine the size of the marker as shown in the RVIZ visualizer
vel_1_mark.scale.x = 1;
vel_1_mark.scale.y = 0.2;
vel_1_mark.scale.z = 0.2;

vel_2_mark.scale.x = 1;
vel_2_mark.scale.y = 0.2;
vel_2_mark.scale.z = 0.2;


// Sets the color of the power supply
vel_1_mark.color.r = 0.0f;
vel_1_mark.color.g = 1.0f;
vel_1_mark.color.b = 0.0f;
vel_1_mark.color.a = 1.0;

vel_2_mark.color.r = 0.0f;
vel_2_mark.color.g = 0.0f;
vel_2_mark.color.b = 1.0f;
vel_2_mark.color.a = 1.0;

// The marker last for the duation of the ros system being up. It will be destroyed
//  one the system is closed.
vel_1_mark.lifetime = ros::Duration();
vel_2_mark.lifetime = ros::Duration();

// Publish the first instance of the marker
vel_1_mark_pub.publish(vel_1_mark);
vel_2_mark_pub.publish(vel_2_mark);
// ********************************************************************


// Main loop of the node
vel_1 = 0;
vel_2 = 0;

std_msgs::Float32 vel_1_float;
std_msgs::Float32 vel_2_float;


    while (ros::ok())
    {
      vel_1_mark.scale.x = vel_1;
      vel_2_mark.scale.x = vel_2;

      vel_1_float.data = vel_1;
      vel_2_float.data = vel_2;

      vel_1_pub.publish(vel_1_float);
      vel_2_pub.publish(vel_2_float);
      vel_1_mark_pub.publish(vel_1_mark);
      vel_2_mark_pub.publish(vel_2_mark);

      ros::spinOnce();		
      r.sleep();
    }

}
