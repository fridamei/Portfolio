#include <ros/ros.h>
#include <planar_robot_simulator/planar_robot_2dof.h> 
#include <sensor_msgs/JointState.h>

#include <std_msgs/Float64MultiArray.h>

Eigen::Vector2d u;

void jointCommandCallback(const std_msgs::Float64MultiArray::ConstPtr& msg)
{
  
  Eigen::Vector2d u_local(msg->data[0], msg->data[1]);
  u = u_local;
  
}


int main(int argc, char **argv)
{
  ros::init(argc, argv, "simulator");
  ros::NodeHandle nh;


/* This is the object that simulates a pendulum */
  PlanarRobotSimulator::PlanarRobot2DOF sim;

  ros::Rate loop_rate(100);
  
    /* Allocate the message */
  sensor_msgs::JointState msg;
  msg.name.push_back("joint_1");
  msg.name.push_back("joint_2");
  msg.position.push_back(0.0);
  msg.position.push_back(0.0);  
  msg.velocity.push_back(0.0);
  msg.velocity.push_back(0.0);

  /* Allocate publishers */
  ros::Publisher joint_state_pub = nh.advertise<sensor_msgs::JointState>("joint_state", 1000);

  /* Allcate subscibers */
  ros::Subscriber sub = nh.subscribe("joint_command", 1000, jointCommandCallback);


  while (ros::ok())
  {
    ros::spinOnce();

    /* This performs one step in the simulation */
    double dt = 1.0/100.0;
    
    sim.step(dt, u);

    /* Set the joint state */
    msg.header.stamp = ros::Time::now();
    
   Eigen::Vector2d q_m = sim.getMotorPosition();
   msg.position[0] = q_m(0);
   msg.position[1] = q_m(1);

   Eigen::Vector2d qd_m = sim.getMotorVelocity();
   msg.velocity[0] = qd_m(0);
   msg.velocity[1] = qd_m(1);  
 
    joint_state_pub.publish(msg);

    /* This creates a window that shows the pendulum */
    sim.draw();
    loop_rate.sleep();
  }

  return 0;
}
