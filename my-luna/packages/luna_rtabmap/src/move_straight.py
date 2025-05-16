#!/usr/bin/env python3

import rospy
from duckietown_msgs.msg import WheelsCmdStamped

def move_straight():
    rospy.init_node('move_straight_node', anonymous=True)
    
    pub = rospy.Publisher('/luna/wheels_driver_node/wheels_cmd', WheelsCmdStamped, queue_size=10)
    
    # Wait for publisher to establish connection
    rospy.sleep(1.0)

    msg = WheelsCmdStamped()
    msg.vel_left = 0.5  # speed
    msg.vel_right = 0.5
    msg.header.stamp = rospy.Time.now()

    rospy.loginfo("Moving straight...")
    pub.publish(msg)

    rospy.sleep(5.0)  # move forward for 5 seconds

    # Stop the bot
    msg.vel_left = 0.0
    msg.vel_right = 0.0
    pub.publish(msg)
    rospy.loginfo("Stopped.")

if __name__ == '__main__':
    try:
        move_straight()
    except rospy.ROSInterruptException:
        pass
