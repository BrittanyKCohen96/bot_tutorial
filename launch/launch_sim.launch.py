import os
 
from ament_index_python.packages import get_package_share_directory
 
 
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
 
from launch.actions import ExecuteProcess
 
 
 
def generate_launch_description():
 
 
    # Include the robot_state_publisher launch file, provided by our own package. Force sim time to be enabled
    # !!! MAKE SURE YOU SET THE PACKAGE NAME CORRECTLY !!!
 
    package_name='bot_tutorial' #<--- CHANGE ME
 
    rsp = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(
                    get_package_share_directory(package_name),'launch','rsp.launch.py'
                )]), launch_arguments={'use_sim_time': 'true'}.items()
    )

    # Use the ros_gz bridge service to spawn the robot

    spawn_entity = ExecuteProcess(
        cmd=[
            'gz', 'service', '-s', '/world/empty/create',
            '--reqtype', 'gz.msgs.EntityFactory',
            '--reptype', 'gz.msgs.Boolean',
            '--timeout', '1000',
            '--req',
            'sdf_filename: "/home/brittc/bot_tut/src/bot_tutorial/description/robot.urdf", name: "bot_model"'
        ],
        output='screen'
    )
 
 
    # Launch them all!
    return LaunchDescription([
        rsp,
        spawn_entity,
    ])