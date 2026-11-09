import rclpy
from rclpy.node import Node 
import time
from rclpy.executors import MultiThreadedExecutor

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

    executor = MultiThreadedExecutor(num_threads=2)
    executor.add_node(node)

    try :
        executor.spin()

    except KeyboardInterrupt:
        pass
    finally:
        executor.shutdown()
        node.destroy_node()
        rclpy.shutdown()

if __name__ == "__main__":
    main()

#  lesson :
# a multi-threaded executor provides worker threads, but callback-group rules still decide 
# whether callbacks may overlap. Your two timers are still in the node’s default mutually exclusive 
# group, so after we fix the code, the slow callback should continue to delay the fast one.
