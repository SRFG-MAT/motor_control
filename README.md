
# SoKoRo-MobileTankControl
source code on jetson nano to control the mobile tank

## checkout and run
- runs on an Nvidia Jetson Nano Board
- local repository should run within the catkin workspace of the device (name="ros_ws" -> ros_ws/src)
- features an implementation in cpp and python to control the motors and do the ROS-communication
- connected GPIO-PINS are: [ENA = 33, IN1 = 35, IN2 = 37, ENB = 38, IN3 = 32, IN4 = 36] (directly connect to motor driver L298N)
- compile and run the cpp-file or start main.py

## tank general infos
- the tank may be loaded with up to 10kg weight
- the tank my be controlled using a ROS-publisher
- the tank currently executes the move-commands without any safety guarantee
- we currently only use the python implementation, cpp works but is not used anywhere

## steps for first installation
- install Ubuntu and ROS
- create a catkin workspace (see the steps below)
- clone this repository into the workspace's src directory
- clone other, required repositories into the src directory
- [OPTIONAL] execute "rosdep install -i --from-paths src" from the workspace to install ROS dependencies
- [OPTIONAL] execute "catkin_make" from the workspace to build all packages in the workspace

## steps to create the catkin workspace with ROS
1) mkdir –p ~/catkin_ws/src
2) cd ~/catkin_ws/src
3) catkin_init_workspace
4) cd ~/catkin_ws/
5) catkin_make
6) source ~/catkin_ws/devel/setup.bash
7) echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
8) catkin_create_pkg beginner_tutorials std_msgs rospy roscpp

## start with
"rosrun motor_control motor_control.py"

## access with
package_name = "motor_control"
IP-Address: "192.168.48.32"
