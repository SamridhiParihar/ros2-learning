import rclpy
from rclpy.node import Node 
from std_msgs.msg import String

class StatusSubscriberNode(Node):
    def __init__(self):
        super().__init__("status_subscriber_node")

        # create a subsriber
        self.subscriber_ = self.create_subscription(String,'/robots/status',self.listener_callback,10)

        self.get_logger().info('Status Subscriber Node has been started.')

    # 3. Uses a callback that receives the message.
    def listener_callback(self, msg):
        # 4. Logs the text from message.data.
        self.get_logger().info(f'I heard: "{msg.data}"')


def main(args=None):
    rclpy.init(args=args)
    
    node = StatusSubscriberNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
