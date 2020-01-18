#!/usr/bin/env python
""" Simple class to subscribe and show an image passed via rosmg on OpenCV    
"""

import cv2
import rospy
from cv_bridge import CvBridge, CvBridgeError
from sensor_msgs.msg import Image as img


class ImageSubscriber(object):
    """ Class for image subscriber """

    def __init__(self):
        """ Constructor """

        rospy.init_node("image_sub_node", anonymous=False)
        self.image_sub = rospy.Subscriber(
            "image_pub_topic", img, self.img_sub_callback)
        self.cvbridge_obj = CvBridge()
        rospy.spin()

    def img_sub_callback(self, callback_data):
        """ Subscriber callback function """
        try:
            ros_img = self.cvbridge_obj.imgmsg_to_cv2(callback_data)
            # Convert CV format to ROS image format
            cv2.imshow('Receving the image...', ros_img)
            if cv2.waitKey(27) == ord('q'):
                cv2.destroyAllWindows()
                rospy.signal_shutdown("user terminated")
        except CvBridgeError as bridgerr:
            print bridgerr


def main():
    "Main function"
    # Initialize the subscriber node and register the callback
    ImageSubscriber()
    rospy.spin()


if __name__ == '__main__':
    try:
        main()
    except rospy.ROSInterruptException as err:
        print err + "subscriber"
