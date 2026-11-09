import rclpy
from rclpy.node import Node 

class TimerNode(Node):
    def __init__(self):
        super().__init__("timer_node")

        # creating a timer 
        self.timer = self.create_timer(1.0, self.timer_callback)

    def timer_callback(self):
        self.get_logger().info("Timer Callback is running")


def main(args=None):
    rclpy.init(args=args)

    node = TimerNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()