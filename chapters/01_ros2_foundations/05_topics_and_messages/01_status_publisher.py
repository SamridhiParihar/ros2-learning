import rclpy
from rclpy.node import Node 
from std_msgs.msg import String

class StatusPublisherNode(Node):
    def __init__(self):
        super().__init__("status_publisher_node")

         # creating publisher 
        self.publisher_ = self.create_publisher(String , '/robots/status', 10)

        # create timer
        self.timer = self.create_timer(1.0,self.timer_callback)

        #log 
        self.get_logger().info('Status Publisher Node has been started.')


    def timer_callback(self):
        self.get_logger().info("Timer Callback is running")

        msg = String()
        msg.data = "Searching for a red cup"

        self.publisher_.publish(msg)
        self.get_logger().info(r'Publishing: "%s"' % msg.data)
    
def main(args=None):

    rclpy.init(args=args)

    node = StatusPublisherNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally :
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()


