import os

from launch.actions import RegisterEventHandler, TimerAction
from launch.event_handlers import OnProcessExit

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


from launch_ros.actions import Node


def generate_launch_description():

    package_name = "adcs_sstl" #package name MAKE SURE IT MATCHES

#sets use sime time to true
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(package_name),'launch','rsp.launch.py')]),
        launch_arguments={'use_sim_time':'true','use_ros2_control':'false'}.items()# 2nd argumnet true-->use ros2 cont, false ->> use gazebo cont
    )
    gazebo_params_file = os.path.join(
            get_package_share_directory(package_name),'config','gazebo_params.yaml'
        )

    
# launches gazebo
# same as 'ros2 launch gazebo_ros gazebo.launch.py'
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'),'launch','gazebo.launch.py')]),
        launch_arguments={'extra_gazebo_args':'--ros-args --params-file '+ gazebo_params_file}.items()#{space after the -file is important}
    )

# spawns entity after opening gazebo
#same as 'ros2 run gazebo_ros spawn_entity.py -topic robot_description -entity bot_name'
    spawn_entity = Node(package='gazebo_ros',executable='spawn_entity.py',
                        arguments=['-topic','robot_description',
                                   '-entity','mybot'],
                        output ='screen' )
    
    
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
    delayed_diff_drive_spawner = TimerAction(
        period=3.0,
        actions=[diff_drive_spawner]
    )

    delayed_joint_broad_spawner = TimerAction(
        period=4.0,  # extra delay to ensure proper startup
        actions=[joint_broad_spawner]
    )



    return LaunchDescription([
    rsp,
    gazebo,
    spawn_entity,
    delayed_diff_drive_spawner,
    delayed_joint_broad_spawner
])



