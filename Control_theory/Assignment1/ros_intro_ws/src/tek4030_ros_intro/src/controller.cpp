#include <ros/ros.h>
#include <sensor_msgs/JointState.h>

#include <std_msgs/Float64MultiArray.h>

#include <planar_robot_simulator/planar_robot_2dof.h>

using namespace PlanarRobotSimulator;
using namespace PlanarRobotSimulator::Parameters;


ros::Publisher* command_pub_global = NULL;

void jointStateCallback(const sensor_msgs::JointState::ConstPtr& msg)
{

  Eigen::Vector2d q_m(msg->position[0], msg->position[1]);
  Eigen::Vector2d qd_m(msg->velocity[0], msg->velocity[1]);
 

  Eigen::Vector2d q_m_set(0.5*M_PI*k_r_1, -0.25*M_PI*k_r_2);  

  Eigen::Vector2d K_p(1.0, 1.0);
  Eigen::Vector2d u = K_p.cwiseProduct(q_m_set-q_m);

  std_msgs::Float64MultiArray output;
  output.data.push_back(u(0));
  output.data.push_back(u(1));

  command_pub_global->publish(output);
}

int main(int argc, char **argv)
{
  ros::init(argc, argv, "controller");
  ros::NodeHandle nh;


  ros::Publisher command_pub = nh.advertise<std_msgs::Float64MultiArray>("joint_command", 1000);
  
  command_pub_global = &command_pub;

  ros::Subscriber sub = nh.subscribe("joint_state", 1000, jointStateCallback);

  ros::spin();

  return 0;
}
