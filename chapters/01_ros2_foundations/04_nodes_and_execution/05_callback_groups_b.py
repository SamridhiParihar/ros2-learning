import rclpy
from rclpy.node import Node 
import time
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup

class TimerNode(Node):

    def __init__(self):
        super().__init__("timer_node")

        # create group
        self.reentrant_group = ReentrantCallbackGroup()


        # create a timer
        self.fast_timer = self.create_timer(
            0.5,
            self.fast_callback,
            callback_group = self.reentrant_group
        )
        self.slow_timer = self.create_timer(
            1,
            self.slow_callback,
            callback_group = self.reentrant_group
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

# lesson : 
# A ReentrantCallbackGroup allows callbacks in the group to overlap,
# including multiple runs of the same timer callback. In our run, slow
# callback runs overlapped because the timer period was shorter than the
# callback duration. They occupied both executor threads at times, delaying
# the fast callback.
#
# Separate MutuallyExclusiveCallbackGroups let the fast and slow callbacks
# overlap with each other while preventing the slow callback from overlapping
# with another run of itself.