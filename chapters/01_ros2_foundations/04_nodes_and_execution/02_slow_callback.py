import rclpy
from rclpy.node import Node 
import time

class TimerNode(Node):

    def __init__(self):
        super().__init__("timer_node")

        # create a timer
        self.fast_timer = self.create_timer(0.5,self.fast_callback)
        self.slow_timer = self.create_timer(1,self.slow_callback)

    def fast_callback(self):
        self.get_logger().info("Fast Timer Callback is running")
    
    def slow_callback(self):
        self.get_logger().info("Slow Timer Callback is started")
        time.sleep(2)
        self.get_logger().info("Slow Timer Callback is finished")
    
def main(args=None):
    rclpy.init(args=args)

    node = TimerNode()

    try :
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()

# lesson : 
# a timer does not create its own thread. It makes a callback ready. 
#The executor runs that callback, and a slow callback can hold up other callbacks
# handled by the same single-threaded executor.