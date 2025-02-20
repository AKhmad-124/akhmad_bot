import os
from launch.actions import RegisterEventHandler, TimerAction
from launch.event_handlers import OnProcessStart

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command

from launch_ros.actions import Node


def generate_launch_description():

    package_name = "akhmad_bot" #package name MAKE SURE IT MATCHES

#sets use sime time to true
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(package_name),'launch','rsp.launch.py')]),
        launch_arguments={'use_sim_time':'false','use_ros2_control':'true'}.items()# 2nd argumnet true-->use ros2 cont, false ->> use gazebo cont
    )


    robot_description = Command(['ros2 param get --hide-type /robot_state_publisher robot_description'])

    controller_params_file = os.path.join(get_package_share_directory(package_name),'config','my_controllers.yaml')


    controller_manager = Node(
        package="controller_manager",
        executable="ros2_control_node",
        parameters=[{'robot_description': robot_description},
                    controller_params_file])

    
    # Diff drive controller spawner
    diff_drive_spawner = Node(
        package="controller_manager",
        executable="spawner.py",
        arguments=["diff_cont"])
    
    
    # joint broadcaster spawner
    joint_broad_spawner = Node(
        package="controller_manager",
        executable="spawner.py",
        arguments=["joint_broad"])
    


    # delay for spawning controllers 
    delayed_controller_manager = TimerAction(
        period=3.0,
        actions=[controller_manager]
    )
    # delay for spawning controllers 
    delayed_diff_drive_spawner = TimerAction(
        period=9.0,
        actions=[diff_drive_spawner]
    )

    delayed_joint_broad_spawner = TimerAction(
        period=11.5,  # extra delay to ensure proper startup
        actions=[joint_broad_spawner]
    )



    return LaunchDescription([
    rsp,
    delayed_controller_manager,
    delayed_diff_drive_spawner,
    delayed_joint_broad_spawner
])



