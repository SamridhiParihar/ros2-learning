import rclpy
from rclpy.node import Node 
import time
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import MutuallyExclusiveCallbackGroup

class TimerNode(Node):

    def __init__(self):
        super().__init__("timer_node")

        # create groups
        self.fast_group = MutuallyExclusiveCallbackGroup()
        self.slow_group = MutuallyExclusiveCallbackGroup()


        # create a timer
        self.fast_timer = self.create_timer(
            0.5,
            self.fast_callback,
            callback_group = self.fast_group
        )
        self.slow_timer = self.create_timer(
            1,
            self.slow_callback,
            callback_group = self.slow_group
        )

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
# separate callback groups let the fast callback run while the slow callback is sleeping.