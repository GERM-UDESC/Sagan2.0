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
    pause = LaunchConfiguration('pause')
    pause_arg = DeclareLaunchArgument(
        'pause',
        default_value='false'
    )

    pos_z = LaunchConfiguration('z')
    pos_z_arg = DeclareLaunchArgument(
        'z',
        default_value='0.15'
    )

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
                                get_package_share_directory('sagan_description'), 'launch'), '/sagan_box.launch.py'])
                        )

    # Spawn Robot
    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
                        arguments=['-topic', 'robot_description',
                                   '-entity', 'sagan',
                                   '-z', pos_z],
                        output='screen')

    return LaunchDescription([
        pause_arg,
        pos_z_arg,
        gazebo,
        sagan_box_desc,
        spawn_entity,
    ])