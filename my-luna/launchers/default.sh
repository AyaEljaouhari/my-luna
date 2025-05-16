#!/bin/bash

source /environment.sh

# Initialize launch file
dt-launchfile-init

# Launch your custom launch file
roslaunch luna_rtabmap rtabmap_luna.launch

# Wait for app to end
dt-launchfile-join
