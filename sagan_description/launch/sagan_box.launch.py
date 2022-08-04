import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch_ros.actions import Node

import xacro


def generate_launch_description():
    
    # Load URDF
    robot_description_path = os.path.join(
        get_package_share_directory('sagan_description'))

    xacro_file = os.path.join(robot_description_path,
                              'robots',
                              'sagan_box.urdf.xacro')

    doc = xacro.parse(open(xacro_file))
    xacro.process_doc(doc)
    robot_description = {'robot_description': doc.toxml()}

    # Robot State Publisher
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    return LaunchDescription([
        node_robot_state_publisher
    ])