# Copyright 2023 Perception for Physical Interaction Laboratory at Poznan University of Technology
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction, IncludeLaunchDescription
from launch.launch_description_sources import FrontendLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def launch_setup(context, *args, **kwargs):
    pkg_prefix = FindPackageShare(LaunchConfiguration('param_file_pkg'))
    config = PathJoinSubstitution([pkg_prefix, LaunchConfiguration('param_file')])

    # apm_interface_node = Node(
    #     name='apm_interface_node',
    #     namespace='',
    #     package='apm_interface',
    #     executable='apm_interface_node',
    #     parameters=[
    #             config
    #     ],
    #     # remappings=[
    #     #         ('', '')
    #     # ],
    #     output='screen',
    #     arguments=['--ros-args', '--log-level', 'info', '--enable-stdout-logs'],
    #     emulate_tty=True
    # )

    raw_vehicle_converter_launch = IncludeLaunchDescription(
        FrontendLaunchDescriptionSource(
            launch_file_path=PathJoinSubstitution([
                FindPackageShare('raw_vehicle_cmd_converter'), 'launch', 'raw_vehicle_converter.launch.xml'
            ]),
        ),
        launch_arguments={
            'converter_param_path': PathJoinSubstitution([
                FindPackageShare('raw_vehicle_cmd_converter'), 'config', 'converter.param.yaml'
            ]),
            'csv_path_accel_map': PathJoinSubstitution([
                FindPackageShare('raw_vehicle_cmd_converter'), 'data', 'default/accel_map.csv'
            ]),
            'csv_path_brake_map': PathJoinSubstitution([
                FindPackageShare('raw_vehicle_cmd_converter'), 'data', 'default/brake_map.cs'
            ]),
            'csv_path_steer_map': PathJoinSubstitution([
                FindPackageShare('raw_vehicle_cmd_converter'), 'data', 'data/default/steer_map.csv'
            ]),
            'max_throttle': '0.4',
            'max_brake': '0.9',
            'max_steer': '10.0',
            'min_steer': '-10.0',
            'convert_accel_cmd': 'true',
            'convert_brake_cmd': 'true',
            'convert_steer_cmd': 'true',
            'input_control_cmd': '/control/command/control_cmd',
            'input_odometry': '/localization/kinematic_state',
            'input_steering': '/vehicle/status/steering_status',
            'output_actuation_cmd': '/control/command/actuation_cmd'
        }.items()
    )

    return [
        # apm_interface_node,
        raw_vehicle_converter_launch
    ]


def generate_launch_description():
    declared_arguments = []

    declared_arguments.append(
        DeclareLaunchArgument(
            'param_file_pkg',
            default_value='apm_vehicle_launch',
            description="Package name which contains param file."
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            'param_file',
            default_value='config/apm_interface.param.yaml',
            description="Param file (relative path)."
        )
    )

    declared_arguments.append(
        DeclareLaunchArgument(
            'vehicle_id',
            default_value='default',
            description="Vehicle ID."
        )
    )
    
    return LaunchDescription([
        *declared_arguments,
        OpaqueFunction(function=launch_setup)
    ])
