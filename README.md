# Duckiebot Autonomous Line Following and 2D Mapping Project

## Project Overview

This project enables a Duckiebot (model DB21M, named "Luna") to attempt autonomous navigation along a continuous white line in a Duckietown environment. Concurrently, it integrates the RTAB-Map algorithm to build a 2D map of the environment using the Duckiebot's monocular camera and wheel encoder odometry. The system is built on ROS (Robot Operating System) and aims to visualize the robot's pose and the generated map in RViz.

**Current State:**

  * **Line Following:** The Duckiebot successfully detects the white line using its camera. However, the current proportional controller is not robust enough to follow curves and tends to drive straight off the track. The robot also does not stop as intended when the white line is lost.
  * **2D Mapping:** RTAB-Map is integrated and configured to receive camera and odometry data. While the project aims to generate a 2D `OccupancyGrid` map, successful visualization of this map in RViz was not achieved during development (an error occurred when attempting to add the "Map" display). Other RViz visualizations (robot model, TF, odometry, pose, image feed) work correctly.

## Prerequisites

Before proceeding, ensure you have the following:

### Hardware

  * **Duckiebot DB21M ("Daffy"):** Fully assembled and functional.
  * **Duckietown Environment:** A track with continuous white lines.
  * **Host PC:** Running Ubuntu 22.04 LTS (recommended for Duckietown compatibility).
      * **ROS Noetic:** Installed on your host PC.

### Software

  * **Duckietown Shell:** Installed and configured on your host PC.
  * **ROS Noetic (on Duckiebot):** Your Duckiebot firmware should be configured for ROS Noetic.
  * **`rtabmap_ros` package:** Installed on your Duckiebot. You might need to install it if it's not present by default.
    ```bash
    # On your Duckiebot terminal (or SSH into it)
    sudo apt update
    sudo apt install ros-noetic-rtabmap-ros
    ```
  * **`cv_bridge`:** This is usually part of ROS, but ensure it's available.
    ```bash
    # On your Duckiebot terminal
    sudo apt install ros-noetic-cv-bridge
    ```

## Setup Instructions

### 1\. Set up Duckietown Shell Environment

If you haven't already, set up your Duckietown shell environment on your host PC. Follow the official Duckietown documentation for this: [https://docs.duckietown.org/daffy/duckiebot\_manual/duckiebot\_setup/index.html](https://www.google.com/search?q=https://docs.duckietown.org/daffy/duckiebot_manual/duckiebot_setup/index.html)

**Important Note:** This project was developed on **Ubuntu 22.04 LTS**. Downgrading might be necessary if you are on a newer version (e.g., 24.04), as newer Ubuntu versions can have compatibility issues with Duckietown's Python environment management.

### 2\. Calibrate your Duckiebot

Accurate calibration is crucial for both line following and mapping.

  * **Camera Calibration:** Calibrate your Duckiebot's camera to correct for lens distortion.
    ```bash
    # On your Host PC, connected to the Duckiebot
    dts duckiebot calibrate_camera <YOUR_DUCKIEBOT_NAME>
    ```
  * **Wheel Calibration:** Calibrate your Duckiebot's wheels for accurate odometry.
    ```bash
    # On your Host PC, connected to the Duckiebot
    dts duckiebot calibrate_wheels <YOUR_DUCKIEBOT_NAME>
    ```
    Ensure the calibration process is successful and the Duckiebot can move straight and turn predictably when tested.

### 3\. Clone the Project Repository

Navigate to your Duckietown workspace's `catkin_ws/src` directory on your **Host PC** and clone the project repository.
This repository (`my-luna`) is expected to contain a ROS package (e.g., named `rluna_tabmap`) with your scripts and launch files.

```bash
# On your Host PC terminal
cd ~/duckietown/catkin_ws/src
git clone https://github.com/AyaEljaouhari/my-luna.git
```

### 4\. Build the Workspace using Duckietown's Development Tools

Use the `dts devel build` command to build your code inside the Duckietown Docker container. This ensures all dependencies are met and the project is built according to Duckietown conventions.

```bash
# On your Host PC terminal, from your Duckietown directory (e.g., ~/duckietown/)
dts devel build -f
```

### 5\. Make Python Nodes Executable

Even when building with `dts devel build`, it's good practice to explicitly make Python scripts executable, as `dts` might not always set these permissions.
*Assume your Python nodes `lane_following_node.py` and `map_publisher_node.py` are located in `~/duckietown/catkin_ws/src/my-luna/rluna_tabmap/scripts/` after cloning.*

```bash
# On your Host PC terminal (these commands will apply to the files in your cloned repo)
chmod +x ~/duckietown/catkin_ws/src/my-luna/rluna_tabmap/scripts/lane_following_node.py
chmod +x ~/duckietown/catkin_ws/src/my-luna/rluna_tabmap/scripts/map_publisher_node.py
```

*(Adjust the path if your scripts are in a different subdirectory within `my-luna`.)*

## Running the Code

Follow these steps to test the line following and mapping functionality:

### 1\. Run RTAB-Map SLAM and Lane Following

Use `dts devel run` to execute your ROS launch file within the Duckietown environment on your Duckiebot. Replace `<YOUR_DUCKIEBOT_NAME>` with your Duckiebot's actual name (e.g., `luna`).

```bash
# On your Host PC terminal, from your Duckietown directory (e.g., ~/duckietown/)
dts devel run -M -- roslaunch rluna_tabmap rluna_tabmap.launch robot_name:=<YOUR_DUCKIEBOT_NAME>
```

This command will:

  * Start `roscore` within the Docker container.
  * Launch the Duckiebot's core ROS nodes (camera, kinematics, joy\_mapper, etc.).
  * Launch your `lane_following_node`.
  * Launch the `rtabmap` node.
  * Launch your `map_publisher_node`.

**Important:** The `rluna_tabmap.launch` file (expected in `~/duckietown/catkin_ws/src/my-luna/rluna_tabmap/launch/`) should look like this:

#### `~/duckietown/catkin_ws/src/my-luna/rluna_tabmap/launch/rluna_tabmap.launch`

```xml
<launch>
  <arg name="robot_name" default="luna" /> 

  <include file="$(find duckietown_vehicles)/launch/$(arg robot_name).launch" />

  <node pkg="rluna_tabmap" type="lane_following_node.py" name="lane_following_node" output="screen">
    <remap from="/luna/joy_mapper_node/car_cmd" to="/$(arg robot_name)/joy_mapper_node/car_cmd" />
    <remap from="/luna/camera_node/image/compressed" to="/$(arg robot_name)/camera_node/image/compressed" />
  </node>

  <node pkg="rtabmap_ros" type="rtabmap" name="rtabmap" output="screen">
    <param name="subscribe_depth" type="bool" value="false" />
    <param name="subscribe_rgb" type="bool" value="true" />
    <param name="subscribe_stereo" type="bool" value="false" />
    <param name="subscribe_rgbd" type="bool" value="false" />
    <param name="subscribe_scan" type="bool" value="false" />
    <param name="subscribe_scan_cloud" type="bool" value="false" />
    <param name="subscribe_odom" type="bool" value="true" /> <remap from="rgb/image" to="/$(arg robot_name)/camera_node/image/compressed" />
    <remap from="rgb/camera_info" to="/$(arg robot_name)/camera_node/camera_info" />
    <remap from="odom" to="/$(arg robot_name)/velocity_to_pose_node/pose" /> <param name="frame_id" type="string" value="$(arg robot_name)/base_link" />
    <param name="rgbd_sync" type="bool" value="true" />
    <param name="approx_sync" type="bool" value="true" />
    <param name="Mem/IncrementalMemory" type="string" value="true" />
    <param name="Mem/InitWMWithUncertainty" type="string" value="false" />
    <param name="RGBD/NeighborLinkRefining" type="string" value="true" />
    <param name="RGBD/StartAtOrigin" type="string" value="true" />
    <param name="Optimizer/GravitySigma" type="string" value="0" />
    <param name="Reg/Force3DoF" type="string" value="true" />
    <param name="Reg/Strategy" type="string" value="1" /> <param name="Vis/MinInliers" type="string" value="20" />
    <param name="Kp/MaxFeatures" type="string" value="500" />
    <param name="Kp/DetectorStrategy" type="string" value="6" /> </node>

  <node pkg="rluna_tabmap" type="map_publisher_node.py" name="map_publisher_node" output="screen"/>

</launch>
```

### 2\. Monitor in RViz (on your Host PC)

Open a terminal on your **Host PC**.

```bash
roslaunch rviz rviz
```

In RViz:

1.  Click "Add" in the "Displays" panel.
2.  Add the following display types and configure their topics (replace `<YOUR_DUCKIEBOT_NAME>` with your Duckiebot's name):
      * **RobotModel:** Add.
      * **TF:** Add.
      * **Odometry:** Topic: `/$(YOUR_DUCKIEBOT_NAME)/velocity_to_pose_node/pose`.
      * **Pose:** Topic: `/$(YOUR_DUCKIEBOT_NAME)/kinematics_node/pose` (or `/$(YOUR_DUCKIEBOT_NAME)/velocity_to_pose_node/pose`, depending on which publishes a nav\_msgs/PoseStamped).
      * **Image:** Topic: `/$(YOUR_DUCKIEBOT_NAME)/camera_node/image/compressed`.
      * **Map:** Topic: `/rtabmap/map` (or `/map`). **Note:** This is the component that gave an error during development. You can still try adding it.
3.  Set the **Fixed Frame** in RViz to `map` or `/$(YOUR_DUCKIEBOT_NAME)/base_link` initially. If you don't see anything, try `odom`.

### 3\. Place Duckiebot on Track and Observe

Place your Duckiebot on the continuous white line track. It should start moving forward and attempt to follow the line. Observe its physical behavior and the visualizations in RViz.

## Expected Behavior and Known Issues

  * **Line Following:**
      * **Expected:** Robot moves forward and attempts to stay centered on the white line.
      * **Actual/Known Issue:** The robot will move forward, and you will see "White line not detected" warnings in the terminal when it's off the line. However, the proportional controller is insufficient for following curves, and the robot will often drive straight through turns. Despite the code, the robot *will not* stop when the line is lost.
  * **2D Mapping & RViz Visualization:**
      * **Expected:** You should see the robot's model, its odometry/pose updates, and the live camera feed in RViz. As the robot moves, RTAB-Map should build an `OccupancyGrid` map, which should appear in the RViz "Map" display.
      * **Actual/Known Issue:** You will see the robot model, TF, odometry, pose, and camera feed in RViz. However, adding the "Map" display to visualize the 2D `OccupancyGrid` will likely result in an error or a blank map, indicating that the map is either not being published correctly by RTAB-Map or not being received/interpreted correctly by RViz in this setup. The dummy `map_publisher_node` provided here may not be correctly interfacing with RTAB-Map's actual output.

## Troubleshooting

  * **Duckietown Docker/Shell Issues:** Refer to the official Duckietown documentation for `dts` commands and environment setup.
  * **"data was not received for 5 seconds" error:** This usually means a critical ROS node isn't publishing data or isn't running.
      * Ensure your Duckiebot's core services are running. You can test `kinematics_node` by using a joystick (`dts start_gui_tools <YOUR_DUCKIEBOT_NAME>`) or running a simple `move_straight.py` script.
      * Check `rosnode list` and `rostopic list` within the Docker container (by running `dts devel cmd <YOUR_DUCKIEBOT_NAME> -- rosnode list`) to confirm all expected nodes and topics are active.
      * Use `rostopic echo <topic_name>` (e.g., `rostopic echo /luna/camera_node/image/compressed`) to check if data is being published.
  * **Robot not moving or acting erratically:**
      * Double-check your wheel and camera calibrations.
      * Ensure the Python scripts are executable (`chmod +x`).
      * Verify the `roslaunch` command uses the correct Duckiebot name.
      * Monitor the `lane_following_node`'s output in the terminal for warnings/errors.
  * **RViz map not showing:**
      * Confirm your host PC can communicate with the Duckiebot's ROS master (check `ROS_MASTER_URI` on your host PC).
      * Ensure the `rtabmap` node and `map_publisher_node` are launched and active within the Docker container.
      * Verify the `map` topic is being published (e.g., `dts devel cmd <YOUR_DUCKIEBOT_NAME> -- rostopic info /rtabmap/map`). If it's not publishing or `map_publisher_node` isn't connected to `rtabmap`'s output, this is the root cause.
      * Check the `Fixed Frame` in RViz settings. Try `map` or `odom`.
      * Look for error messages in the RViz display panel.

## Acknowledgements

This project was developed as part of a robotics course and benefited from the Duckietown educational platform. Special thanks to Kristina for invaluable assistance in debugging and resolving environment-related issues (Ubuntu version, lost drivers, ROS 1 vs. ROS 2 compatibility).

-----
