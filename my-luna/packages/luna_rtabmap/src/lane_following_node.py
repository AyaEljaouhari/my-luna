#!/usr/bin/env python3

import rospy
import cv2
import numpy as np
from cv_bridge import CvBridge
from sensor_msgs.msg import CompressedImage
from duckietown_msgs.msg import Twist2DStamped

class LaneFollower:
    def __init__(self):
        self.node_name = "lane_following_node"
        rospy.init_node(self.node_name)

        # Parameters
        self.bridge = CvBridge()
        self.cmd_pub = rospy.Publisher("/luna/joy_mapper_node/car_cmd", Twist2DStamped, queue_size=1)
        rospy.Subscriber("/luna/camera_node/image/compressed", CompressedImage, self.process_image)

        rospy.loginfo("[%s] Initialized." % self.node_name)

    def process_image(self, msg):
        try:
            img = self.bridge.compressed_imgmsg_to_cv2(msg, "bgr8")
        except Exception as e:
            rospy.logerr("Could not convert image: %s", e)
            return

        # Resize and crop
        h, w = img.shape[:2]
        crop_img = img[int(h/2):h, 0:w]  # Lower half

        # Convert to HSV
        hsv = cv2.cvtColor(crop_img, cv2.COLOR_BGR2HSV)
        
        # Define white color mask
        lower_white = np.array([0, 0, 200])
        upper_white = np.array([180, 25, 255])
        mask = cv2.inRange(hsv, lower_white, upper_white)

        # Centroid calculation
        M = cv2.moments(mask)
        if M["m00"] > 0:
            cx = int(M["m10"]/M["m00"])
            cy = int(M["m01"]/M["m00"])

            # Error from center
            error = cx - w // 2

            # Simple proportional controller
            k_p = 0.005
            angular = -float(error) * k_p
            linear = 0.2  # Constant forward speed

            # Publish command
            cmd = Twist2DStamped()
            cmd.v = linear
            cmd.omega = angular
            self.cmd_pub.publish(cmd)
        else:
            rospy.logwarn("White line not detected")

if __name__ == "__main__":
    lane_follower = LaneFollower()
    rospy.spin()
