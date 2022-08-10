import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    # Declare Launch file Arguments
    launch_args = []

    pause = LaunchConfiguration('pause')
    pause_arg = DeclareLaunchArgument(
        'pause',
        default_value='false'
    )
    launch_args.append(pause_arg)

    pos_x = LaunchConfiguration('x')
    pos_x_arg = DeclareLaunchArgument(
        'x',
        default_value='0.0'
    )
    launch_args.append(pos_x_arg)

    pos_y = LaunchConfiguration('y')
    pos_y_arg = DeclareLaunchArgument(
        'y',
        default_value='0.0'
    )
    launch_args.append(pos_y_arg)

    pos_z = LaunchConfiguration('z')
    pos_z_arg = DeclareLaunchArgument(
        'z',
        default_value='0.15'
    )
    launch_args.append(pos_z_arg)


    # Load World file
    world_file = PathJoinSubstitution(
        [FindPackageShare("sagan_gazebo"),
        "worlds",
        "empty_world.world"],
    )

    # Start Gazebo Simulation
    gazebo = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
                    launch_arguments = {'pause': pause, 'world': world_file}.items(),
             )
    
    # Load Robot Description
    sagan_box_desc = IncludeLaunchDescription(
                            PythonLaunchDescriptionSource([os.path.join(
                                get_package_share_directory('sagan_description'), 'launch'), '/sagan_box.launch.py']),
                                launch_arguments = {'sim_gazebo': 'true', }.items(),
                        )

    # Spawn Robot
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'sagan',
                                   '-x', pos_x,
                                   '-y', pos_y,
                                   '-z', pos_z],
                        output='screen')

    return LaunchDescription(
        launch_args
        +
        [
            pause_arg,
            gazebo,
            sagan_box_desc,
            spawn_entity
        ]
    )