#!/bin/bash
source /environment.sh
dt-launchfile-init
roslaunch luna_rtabmap lane_following.launch
dt-launchfile-join
