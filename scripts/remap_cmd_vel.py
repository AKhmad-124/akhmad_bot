#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class ControllerRemapNode(Node):
    def __init__(self):
        super().__init__('controller_remap_node')
        
        # Subscriber to listen to the controller outputs (can be customized based on actual topic names)
        self.create_subscription(
            Twist,
            '/diff_cont/cmd_vel_unstamped',  # Replace with your controller's output topic
            self.listener_callback,
            10
        )
        
        # Publisher to remap to /cmd_vel
        self.cmd_vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        
        self.get_logger().info('Controller Remap Node has started.')

    def listener_callback(self, msg):
        # Simply publish the received message to the /cmd_vel topic
        self.get_logger().info('Received message on /diff_cont/cmd_vel_unstamped, remapping to /cmd_vel.')
        self.cmd_vel_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    
    remap_node = ControllerRemapNode()
    
    rclpy.spin(remap_node)
    
    remap_node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
