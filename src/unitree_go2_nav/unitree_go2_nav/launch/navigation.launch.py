from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution, Command
from launch.conditions import IfCondition
from launch_ros.substitutions import FindPackageShare
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.parameter_descriptions import ParameterValue



def generate_launch_description():

    use_sim_time = LaunchConfiguration('use_sim_time')

    return LaunchDescription([

        DeclareLaunchArgument(
            name='use_sim_time',
            default_value='false',
            choices=['true','false'],
        ),

        DeclareLaunchArgument(
            name='use_rviz',
            default_value='false',
            choices=['true','false'],
            description='Open RVIZ for Go2 visualization'
        ),

        DeclareLaunchArgument(
            name='use_nav2_rviz',
            default_value='false',
            choices=['true','false'],
            description='Open RVIZ for Nav2 visualization'
        ),
           # -------------------------------------------------
        # TF 1: odom -> base_link
        # -------------------------------------------------     
        
        Node(
            package='robot_localization',
            executable='ekf_node',
            name='ekf_filter_node',
            output='screen',
            parameters=[
                PathJoinSubstitution([
                    FindPackageShare('unitree_go2_nav'),
                    'config',
                    'ekf_2d.yaml'
                ])
            ]
        ),
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            name='utlidar_static_tf',
            arguments=[
                '0', '0', '0',        # x y z  (anpassen falls nötig)
                '0', '0', '0',        # roll pitch yaw
                'base_link',
                'utlidar_lidar'
            ],
            output='screen'
        ),
        # -------------------------------------------------
        # TF 2: base_link -> trunk -> sensor_frames (URDF)
        # -------------------------------------------------
       # Node(
       #     package='robot_state_publisher',
       #     executable='robot_state_publisher',
       #     name='robot_state_publisher',
       #     output='screen',
       #     parameters=[{
       #         'use_sim_time': use_sim_time,
       #         'robot_description': ParameterValue(
       #             Command([
       #                 'cat ',
       #                 '/home/ba/navigation_ws/src/unitree_go2_nav/go2_description/urdf/go2_description.urdf'
       #             ]),
       #             value_type=str
       #         )
       #     }],
       # ),

        # -------------------------------------------------
        # Nav goal sender
        # -------------------------------------------------
        Node(
            package='unitree_go2_nav',
            executable='navToPose',
            output='screen',
            remappings=[
                ('odom', '/utlidar/robot_odom'),
                ('cmd_vel_nav', 'cmd_vel_smoothed')
            ],
        ),

        # -------------------------------------------------
        # Nav2 RVIZ
        # -------------------------------------------------
        #IncludeLaunchDescription(
        #    PythonLaunchDescriptionSource(
        #        PathJoinSubstitution([
        #            FindPackageShare('nav2_bringup'),
        #            'launch',
        #            'rviz_launch.py'
        #        ])
        #    ),
        #    condition=IfCondition(LaunchConfiguration('use_nav2_rviz')),
        #),
    ])

