# turtlebot3
# Overview
This ROS node controls a TurtleBot3 robot to move linearly to a specified target point using odometry data.

# Features
Proportional controller for linear velocity
Distance tolerance check (10 cm)
Velocity limiting for safety
Real-time distance logging

# Requirements
ROS
TurtleBot3 packages
Python 3

# Usage
Clone this repository to your ROS workspace
Build the package: catkin_make
Run the node: rosrun your_package_name turtlebot3_linear_controller.py
The robot will attempt to move to the predefined target point (2.0m in x, 1.5m in y).

# Parameters
Target point can be modified in the __main__ section
Distance tolerance and speed coefficients can be adjusted in the code
