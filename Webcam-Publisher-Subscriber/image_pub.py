#!/usr/bin/env python
""" Simple class to publish image read from OpenCV on to rosmsg format
"""

import rospy
import cv2
from sensor_msgs.msg import Image as img
from cv_bridge import CvBridge, CvBridgeError


class ImagePublisher(object):
    """ Class to define member functions for image publisher """

    def __init__(self):
        """ Constructor """
        rospy.init_node('img_pub_node', anonymous=True)
        self.image_pub = rospy.Publisher("image_pub_topic", img, queue_size=20)
        self.cvbridge_obj = CvBridge()
        self.videostream = cv2.VideoCapture(0)

    def img_pub_node(self):
        """ Publisher helper function """

        if self.videostream is None or not self.videostream.isOpened():
            print ("Camera open failed")
            rospy.signal_shutdown("Camera unavailable")

        while not rospy.is_shutdown():
            ret, cv_img = self.videostream.read()
            try:
                if ret is True:
                    # Convert CV format to ROS image format
                    ros_img = self.cvbridge_obj.cv2_to_imgmsg(
                        cv_img, encoding="passthrough")
                    self.image_pub.publish(ros_img)
                    #rate = rospy.Rate(1)
                    # rate.sleep()
                else:
                    print "Video stream read failed"
                    continue

            except CvBridgeError as bridgerr:
                print(bridgerr)


def main():
    "Main function"

    # Initialize the publisher node and call the publiser helper
    image_publisher_obj = ImagePublisher()
    image_publisher_obj.img_pub_node()
    rospy.spin()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException as err:
        print (err + "publisher")
