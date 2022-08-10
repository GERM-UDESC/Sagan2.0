# sagan_control

ROS2 Control configuration and launch files.

## Differential Drive Controller at Gazebo Simulator

First, start the Gazebo Simulation:
```
ros2 launch sagan_gazebo box_sagan_empty.launch.py
```

Set hardware interfaces to active state (as described in this [issue](https://github.com/ros-controls/gazebo_ros2_control/issues/131)):
```
ros2 service call /controller_manager/set_hardware_component_state controller_manager_msgs/srv/SetHardwareComponentState '{name: ''GazeboSystem, target_state: {id: 3, label: ""}}'
```

Launch controllers:
```
ros2 launch sagan_control sagan_diff_drive.launch.py
```

Use teleop if you want to use the keyboard to control the robot:
```
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args --remap cmd_vel:=sagan_diff_drive_controller/cmd_vel_unstamped
```