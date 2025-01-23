import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource


from launch_ros.actions import Node


def generate_launch_description():

    package_name = "akhmad_bot" #package name MAKE SURE IT MATCHES

#sets use sime time to true
    rsp = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory(package_name),'launch','rsp.launch.py'
        )]),launch_arguments={'use_sim_time':'true'}.items()
    )
    
# launches gazebo
# same as 'ros2 launch gazebo_ros gazebo.launch.py'
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'),'launch','gazebo.launch.py'
        )])
    )

# spawns entity after opening gazebo
#same as 'ros2 run gazebo_ros spawn_entity.py -topic robot_description -entity bot_name'
    spawn_entity = Node(package='gazebo_ros',executable='spawn_entity.py',
                        arguments=['-topic','robot_description',
                                   '-entity','mybot'],
                                  output ='screen' )
    return LaunchDescription([
    rsp,
    gazebo,
    spawn_entity

])



