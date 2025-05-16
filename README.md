# my-luna

This is my custom Duckietown ROS workspace (`my-luna`) with multiple packages including RTAB-Map SLAM.

## Structure

- `src/`: Contains all ROS packages
- `rluna_tabmap/`: RTAB-Map integration
- Other folders: [describe any additional functionality]

## Usage

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
