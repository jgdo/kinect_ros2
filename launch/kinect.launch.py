from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch_ros.actions import Node


def prefixed_frame(suffix):
    return PythonExpression(
        [
            "'",
            LaunchConfiguration("tf_prefix"),
            "' + ('/' if '",
            LaunchConfiguration("tf_prefix"),
            "' else '') + '",
            LaunchConfiguration("camera"),
            suffix,
            "'",
        ]
    )


def generate_launch_description():
    camera_link = prefixed_frame("_link")
    depth_frame = prefixed_frame("_depth_frame")
    rgb_frame = prefixed_frame("_rgb_frame")
    depth_optical_frame = prefixed_frame("_depth_optical_frame")
    rgb_optical_frame = prefixed_frame("_rgb_optical_frame")

    return LaunchDescription(
        [
            DeclareLaunchArgument("camera", default_value="kinect"),
            DeclareLaunchArgument("tf_prefix", default_value=""),
            Node(
                package="kinect_ros2",
                executable="kinect_ros2_node",
                name="kinect_ros2",
            ),
            Node(
                package="tf2_ros",
                executable="static_transform_publisher",
                name="depth_frame_static_tf",
                arguments=[
                    "0", "0.025", "0", "0", "0", "0", "1",
                    camera_link, depth_frame,
                ],
            ),
            Node(
                package="tf2_ros",
                executable="static_transform_publisher",
                name="rgb_frame_static_tf",
                arguments=[
                    "0", "0", "0", "0", "0", "0", "1",
                    camera_link, rgb_frame,
                ],
            ),
            Node(
                package="tf2_ros",
                executable="static_transform_publisher",
                name="depth_optical_frame_static_tf",
                arguments=[
                    "0", "0", "0", "-0.5", "0.5", "-0.5", "0.5",
                    depth_frame, depth_optical_frame,
                ],
            ),
            Node(
                package="tf2_ros",
                executable="static_transform_publisher",
                name="rgb_optical_frame_static_tf",
                arguments=[
                    "0", "0", "0", "-0.5", "0.5", "-0.5", "0.5",
                    rgb_frame, rgb_optical_frame,
                ],
            ),
        ]
    )
