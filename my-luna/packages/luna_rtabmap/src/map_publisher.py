#!/usr/bin/env python3

import rospy
from nav_msgs.msg import OccupancyGrid

def publish_map():
    rospy.init_node('map_publisher_node', anonymous=True)
    pub = rospy.Publisher('/rtabmap/map', OccupancyGrid, queue_size=10)

    rate = rospy.Rate(1)  # Publish 1 Hz
    map_msg = OccupancyGrid()
    
    # Fill in the map header/frame_id and dummy data
    map_msg.header.frame_id = "map"
    map_msg.info.resolution = 0.05  # 5 cm/pixel
    map_msg.info.width = 10
    map_msg.info.height = 10
    map_msg.info.origin.position.x = 0.0
    map_msg.info.origin.position.y = 0.0
    map_msg.data = [0] * (10 * 10)  # Dummy flat map with all free space

    while not rospy.is_shutdown():
        map_msg.header.stamp = rospy.Time.now()
        pub.publish(map_msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        publish_map()
    except rospy.ROSInterruptException:
        pass
