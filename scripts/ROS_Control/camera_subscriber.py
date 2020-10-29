#!/usr/bin/env python
import rospy
import pcl
from sensor_msgs.msg import PointCloud2
import sensor_msgs.point_cloud2 as pc2
#import ros_numpy # maybe not working for ROS melodic


def cam1_color_points_callback(data):
    print("I heard something from cam1!")
    #pc = ros_numpy.numpify(data)
    #points=np.zeros((pc.shape[0],3))
    #points[:,0]=pc['x']
    #points[:,1]=pc['y']
    #points[:,2]=pc['z']
    #p = pcl.PointCloud(np.array(points, dtype=np.float32))


def cam2_color_points_callback(data):
    print("I heard something from cam2!")

    #pc = ros_numpy.numpify(data)
    #points=np.zeros((pc.shape[0],3))
    #points[:,0]=pc['x']
    #points[:,1]=pc['y']
    #points[:,2]=pc['z']
    #p = pcl.PointCloud(np.array(points, dtype=np.float32))


if __name__ == '__main__':

    rospy.init_node('realsense-ros', anonymous=True)
    rospy.Subscriber('/cam_1/depth/color/points', PointCloud2, cam1_color_points_callback)
    rospy.Subscriber('/cam_2/depth/color/points', PointCloud2, cam2_color_points_callback)

    rospy.spin()
