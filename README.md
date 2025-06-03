Project Overview

This project enables a Duckiebot (model DB21M, named "Luna") to attempt autonomous navigation along a continuous white line in a Duckietown environment. Concurrently, it integrates the RTAB-Map algorithm to build a 2D map of the environment using the Duckiebot's monocular camera and wheel encoder odometry. The system is built on ROS (Robot Operating System) and aims to visualize the robot's pose and the generated map in RViz.

Current State:

Line Following: The Duckiebot successfully detects the white line using its camera. However, the current proportional controller is not robust enough to follow curves and tends to drive straight off the track. The robot also does not stop as intended when the white line is lost.

2D Mapping: RTAB-Map is integrated and configured to receive camera and odometry data. While the project aims to generate a 2D OccupancyGrid map, successful visualization of this map in RViz was not achieved during development (an error occurred when attempting to add the "Map" display). Other RViz visualizations (robot model, TF, odometry, pose, image feed) work correctly.
Prerequisites
Before proceeding, ensure you have the following:

Hardware
Duckiebot DB21M ("Daffy"): Fully assembled and functional.
Duckietown Environment: A track with continuous white lines.
Host PC: Running Ubuntu 22.04 LTS (recommended for Duckietown compatibility).
ROS Noetic: Installed on your host PC.
Software
Duckietown Shell: Installed and configured on your host PC.
ROS Noetic (on Duckiebot): Your Duckiebot firmware should be configured for ROS Noetic.
rtabmap_ros package: Installed on your Duckiebot. You might need to install it if it's not present by default.
Bash

# On your Duckiebot terminal (or SSH into it)
sudo apt update
sudo apt install ros-noetic-rtabmap-ros
cv_bridge: This is usually part of ROS, but ensure it's available.
Bash

# On your Duckiebot terminal
sudo apt install ros-noetic-cv-bridge
Setup Instructions
1. Set up Duckietown Shell Environment
If you haven't already, set up your Duckietown shell environment on your host PC. Follow the official Duckietown documentation for this: https://docs.duckietown.org/daffy/duckiebot_manual/duckiebot_setup/index.html

Important Note: This project was developed on Ubuntu 22.04 LTS. Downgrading might be necessary if you are on a newer version (e.g., 24.04), as newer Ubuntu versions can have compatibility issues with Duckietown's Python environment management.

2. Calibrate your Duckiebot
Accurate calibration is crucial for both line following and mapping.

Camera Calibration: Calibrate your Duckiebot's camera to correct for lens distortion.
Bash

# On your Host PC, connected to the Duckiebot
dts duckiebot calibrate_camera <YOUR_DUCKIEBOT_NAME>
Wheel Calibration: Calibrate your Duckiebot's wheels for accurate odometry.
Bash

# On your Host PC, connected to the Duckiebot
dts duckiebot calibrate_wheels <YOUR_DUCKIEBOT_NAME>
Ensure the calibration process is successful and the Duckiebot can move straight and turn predictably when tested.
3. Clone the Project Repository on your Duckiebot
SSH into your Duckiebot. If you don't have a ROS workspace, create one. Then, clone the project repository into the src directory of your catkin workspace.

Bash

# SSH into your Duckiebot
ssh <YOUR_DUCKIEBOT_NAME>.local

# Create workspace directories if they don't exist
mkdir -p ~/catkin_ws/src
cd ~/catkin_ws/src

# Clone the repository
git clone https://github.com/AyaEljaouhari/my-luna.git
4. Make Python Nodes Executable
Navigate into the cloned repository's scripts directory and make the Python nodes executable.

Bash

cd ~/catkin_ws/src/my-luna/scripts/
chmod +x lane_following_node.py
chmod +x map_publisher_node.py
5. Build the Workspace
Now, build your ROS workspace to compile any necessary files and make the new nodes discoverable by ROS.

Bash

cd ~/catkin_ws/
catkin_make

# Source the workspace setup file (add to .bashrc for persistence)
echo "source ~/catkin_ws/devel/setup.bash" >> ~/.bashrc
source ~/.bashrc
Running the Code
Follow these steps to test the line following and mapping functionality:

1. Start ROS on the Duckiebot
First, ensure roscore is running on your Duckiebot.

Bash

# On your Duckiebot terminal
roscore
Alternatively, you can start roscore on your host PC if configured for remote ROS communication, but launching nodes directly on the Duckiebot is often simpler for development.

2. Launch the Project Nodes
Open a new terminal on your Duckiebot (or SSH into it again).

Bash

# On your Duckiebot terminal
source ~/catkin_ws/devel/setup.bash
roslaunch my_luna duckiebot_mapping.launch robot_name:=<YOUR_DUCKIEBOT_NAME>
Important: Replace <YOUR_DUCKIEBOT_NAME> with your Duckiebot's actual name (e.g., luna).

This command will launch:

The Duckiebot's core ROS nodes (camera, kinematics, joy_mapper, etc.).
Your lane_following_node.
The rtabmap node.
Your map_publisher_node.
3. Monitor in RViz (on your Host PC)
Open a terminal on your Host PC.

Bash

roslaunch rviz rviz
In RViz:

Click "Add" in the "Displays" panel.
Add the following display types and configure their topics (replace <YOUR_DUCKIEBOT_NAME> with your Duckiebot's name):
RobotModel: Add.
TF: Add.
Odometry: Topic: /$(YOUR_DUCKIEBOT_NAME)/kinematics_node/odom (or similar).
Pose: Topic: /$(YOUR_DUCKIEBOT_NAME)/kinematics_node/pose (or similar).
Image: Topic: /$(YOUR_DUCKIEBOT_NAME)/camera_node/image/compressed (or /$(YOUR_DUCKIEBOT_NAME)/camera_node/image if uncompressed).
Map: Topic: /rtabmap/map (or /map). Note: This is the component that gave an error during development. You can still try adding it.
Set the Fixed Frame in RViz to map or /$(YOUR_DUCKIEBOT_NAME)/base_link initially. If you don't see anything, try odom.
4. Place Duckiebot on Track and Observe
Place your Duckiebot on the continuous white line track. It should start moving forward and attempt to follow the line. Observe its physical behavior and the visualizations in RViz.

Expected Behavior and Known Issues
Line Following:
Expected: Robot moves forward and attempts to stay centered on the white line.
Actual/Known Issue: The robot will move forward, and you will see "White line not detected" warnings in the terminal when it's off the line. However, the proportional controller is insufficient for following curves, and the robot will often drive straight through turns. Despite the code, the robot will not stop when the line is lost.
2D Mapping & RViz Visualization:
Expected: You should see the robot's model, its odometry/pose updates, and the live camera feed in RViz. As the robot moves, RTAB-Map should build an OccupancyGrid map, which should appear in the RViz "Map" display.
Actual/Known Issue: You will see the robot model, TF, odometry, pose, and camera feed in RViz. However, adding the "Map" display to visualize the 2D OccupancyGrid will likely result in an error or a blank map, indicating that the map is either not being published correctly by RTAB-Map or not being received/interpreted correctly by RViz in this setup. The dummy map_publisher_node provided here may not be correctly interfacing with RTAB-Map's actual output.
Troubleshooting
"data was not received for 5 seconds" error: This usually means a critical ROS node isn't publishing data or isn't running.
Ensure roscore is running.
Verify your Duckiebot's core services are running. You can test kinematics_node by using a joystick (dts start_gui_tools <YOUR_DUCKIEBOT_NAME>) or running a simple move_straight.py script.
Check rosnode list and rostopic list on your Duckiebot to confirm all expected nodes and topics are active.
Use rostopic echo <topic_name> (e.g., rostopic echo /luna/camera_node/image/compressed) to check if data is being published.
Robot not moving or acting erratically:
Double-check your wheel and camera calibrations.
Ensure the Python scripts are executable (chmod +x).
Verify the roslaunch command uses the correct Duckiebot name.
Monitor the lane_following_node's output in the terminal for warnings/errors.
RViz map not showing:
Confirm roscore is running on the Duckiebot and your host PC can communicate with it (check ROS_MASTER_URI).
Ensure the rtabmap node and map_publisher_node are launched and active (rosnode list).
Verify the map topic is being published (e.g., rostopic info /rtabmap/map). If it's not publishing or map_publisher_node isn't connected to rtabmap's output, this is the root cause.
Check the Fixed Frame in RViz settings. Try map or odom.
Look for error messages in the RViz display panel.
Acknowledgements
This project was developed as part of a robotics course and benefited from the Duckietown educational platform. Special thanks to Kristina for invaluable assistance in debugging and resolving environment-related issues (Ubuntu version, lost drivers, ROS 1 vs. ROS 2 compatibility).


_______________________________
3. Create a ROS Workspace on your Duckiebot
SSH into your Duckiebot. If you don't have a ROS workspace, create one:

Bash

# SSH into your Duckiebot
ssh <YOUR_DUCKIEBOT_NAME>.local

# Create workspace directories
Clone this repo and build the workspace:

```bash
git clone https://github.com/<your-username>/my-luna.git
cd my-luna
catkin_make
source devel/setup.bash

2. Build the workspace using Duckietown's development tools

dts devel build -f

This builds your code inside the Docker container, following Duckietown conventions.
3. Run RTAB-Map SLAM (example launch)

Assuming your Duckiebot is named luna:

dts devel run -M -- roslaunch rluna_tabmap rluna_tabmap.launch

Launch file topics:

    /luna/camera_node/image/compressed

    /luna/velocity_to_pose_node/pose
