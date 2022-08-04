import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import OpaqueFunction, DeclareLaunchArgument
from launch.substitutions import Command, FindExecutable, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def launch_setup(context, *args, **kwargs):

    # Declare Launch file Arguments
    gazebo = LaunchConfiguration('gazebo')

    # Load URDF with Xacro
    robot_description_content = Command(
        [
            PathJoinSubstitution([FindExecutable(name='xacro')]),
            " ",
            PathJoinSubstitution([FindPackageShare('sagan_description'), 'robots', 'sagan_box.urdf.xacro']),
            " ",
            "gazebo:=",
            gazebo,
            " ",
        ]
    )
    robot_description = {"robot_description": robot_description_content}

    # Robot State Publisher
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    return [
        node_robot_state_publisher
    ]


def generate_launch_description():

    gazebo_arg = DeclareLaunchArgument(
        'gazebo',
        default_value='True'
    )

    return LaunchDescription([
        gazebo_arg,
        OpaqueFunction(function=launch_setup)
    ])