"""
全体起動ランチファイル:
  1. ros_tcp_endpoint  — Quest から TCP 接続を受ける
  2. ik_node           — Quest の PoseStamped → pyroki IK → JointTrajectory

OpenArm 本体は別途 openarm.bimanual.launch.py で起動しておくこと。
CAN も事前に configure-socketcan しておくこと。
"""

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    ros_ip_arg = DeclareLaunchArgument(
        "ros_ip",
        default_value="0.0.0.0",
        description="IP address for ros_tcp_endpoint to bind",
    )

    ros_tcp_port_arg = DeclareLaunchArgument(
        "ros_tcp_port",
        default_value="10000",
        description="Port for ros_tcp_endpoint",
    )

    teleop_venv_arg = DeclareLaunchArgument(
        "teleop_venv",
        default_value="/home/eig-01/teleop_venv/lib/python3.12/site-packages",
        description="Path to teleop_venv site-packages (for pyroki, jaxls, teleop_xr)",
    )

    # ros_tcp_endpoint node
    tcp_endpoint = Node(
        package="ros_tcp_endpoint",
        executable="default_server_endpoint",
        name="ros_tcp_endpoint",
        output="screen",
        parameters=[
            {"ROS_IP": LaunchConfiguration("ros_ip")},
            {"ROS_TCP_PORT": 10000},
        ],
    )

    # IK node — needs teleop_venv on PYTHONPATH
    ik_node = Node(
        package="openarm_teleop",
        executable="ik_node",
        name="quest_teleop_ik",
        output="screen",
        additional_env={
            "PYTHONPATH": LaunchConfiguration("teleop_venv"),
        },
    )

    return LaunchDescription(
        [
            ros_ip_arg,
            ros_tcp_port_arg,
            teleop_venv_arg,
            tcp_endpoint,
            ik_node,
        ]
    )
