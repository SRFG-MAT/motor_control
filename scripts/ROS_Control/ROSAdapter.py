#!/usr/bin/env python

import rospy
from std_msgs.msg import String

#----------------------------------------------------------
# this script features an example implementation of ROS communication
# publisher will post some data to the node
# subscriber will listen until node is stopped
# callback is called whenever subscriber listens to a new value
# see ROS tutorial: http://wiki.ros.org/ROS/Tutorials/WritingPublisherSubscriber%28python%29
#----------------------------------------------------------

#----------------------------------------------------------
# publish (talk)
#----------------------------------------------------------
def publish():
    pub = rospy.Publisher('chatter', String, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()
        rospy.loginfo(hello_str)
        pub.publish(hello_str)
        rate.sleep()

#----------------------------------------------------------
# callback for subscribe (listen)
#----------------------------------------------------------
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.data)
    
#----------------------------------------------------------
# subscribe (listen)
#----------------------------------------------------------
def subscribe():

    # ROS-nodes are uniquely named. If two nodes with the same name
    # are launched, the previous one is kicked off. The anonymous=True
    # flag means that rospy will choose a unique name
    # for our 'listener' node so that multiple listeners can run simultaneously.
    rospy.init_node('listener', anonymous=True)

    rospy.Subscriber("chatter", String, callback)
 
    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()
