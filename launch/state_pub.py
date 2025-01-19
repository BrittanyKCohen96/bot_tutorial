from math import sin, cos, pi
import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster, TransformStamped


class DifferentialDriveStatePublisher(Node):
    def __init__(self):
        rclpy.init()
        super().__init__('differential_drive_state_publisher')

        qos_profile = QoSProfile(depth=10)
        self.joint_pub = self.create_publisher(JointState, 'joint_states', qos_profile)
        self.broadcaster = TransformBroadcaster(self, qos=qos_profile)

        self.get_logger().info(f"{self.get_name()} started")

        degree = pi / 180.0
        loop_rate = self.create_rate(30)  # 30 Hz update rate

        # Robot state
        left_wheel_angle = 0.0
        right_wheel_angle = 0.0
        wheel_speed = degree * 10  # Arbitrary angular velocity for wheels
        angle = 0.0

        # Message declarations
        odom_trans = TransformStamped()
        odom_trans.header.frame_id = 'odom'
        odom_trans.child_frame_id = 'base_link'

        joint_state = JointState()

        try:
            while rclpy.ok():
                rclpy.spin_once(self)

                # Update joint_state
                now = self.get_clock().now()
                joint_state.header.stamp = now.to_msg()
                joint_state.name = ['left_wheel_joint', 'right_wheel_joint']
                joint_state.position = [left_wheel_angle, right_wheel_angle]

                # Update odom transform
                odom_trans.header.stamp = now.to_msg()
                odom_trans.transform.translation.x = cos(angle) * 0.5  # Arbitrary circular motion
                odom_trans.transform.translation.y = sin(angle) * 0.5
                odom_trans.transform.translation.z = 0.0
                odom_trans.transform.rotation = euler_to_quaternion(0, 0, angle)

                # Publish joint state and transform
                self.joint_pub.publish(joint_state)
                self.broadcaster.sendTransform(odom_trans)

                # Update angles for next iteration
                left_wheel_angle += wheel_speed
                right_wheel_angle += wheel_speed
                angle += wheel_speed * 0.01  # Simulate slow rotation of the robot

                loop_rate.sleep()

        except KeyboardInterrupt:
            pass


def euler_to_quaternion(roll, pitch, yaw):
    """
    Converts Euler angles (roll, pitch, yaw) to a quaternion.
    """
    qx = sin(roll / 2) * cos(pitch / 2) * cos(yaw / 2) - cos(roll / 2) * sin(pitch / 2) * sin(yaw / 2)
    qy = cos(roll / 2) * sin(pitch / 2) * cos(yaw / 2) + sin(roll / 2) * cos(pitch / 2) * sin(yaw / 2)
    qz = cos(roll / 2) * cos(pitch / 2) * sin(yaw / 2) - sin(roll / 2) * sin(pitch / 2) * cos(yaw / 2)
    qw = cos(roll / 2) * cos(pitch / 2) * cos(yaw / 2) + sin(roll / 2) * sin(pitch / 2) * sin(yaw / 2)
    return Quaternion(x=qx, y=qy, z=qz, w=qw)


def main():
    node = DifferentialDriveStatePublisher()


if __name__ == '__main__':
    main()
