import rclpy
from rclpy.node import Node
from robot_interfaces.srv import AddTwoFloats

class ServiceClient(Node):
    def __init__(self):
        super().__init__("service_client_node")

        # creating service client
        self.client_ = self.create_client(
            AddTwoFloats,
            "/add_two_floats"
        )

        self.get_logger().info('Service Client Node has been started.')


    def send_request(self, a, b):
        
        # wait until server is available 
        while not self.client_.wait_for_service(timeout_sec=1.0):
            if not rclpy.ok():
                self.get_logger().error('Interrupted while waiting. Exiting.')
                return
            self.get_logger().info('Service not available, waiting again...')

        request = AddTwoFloats.Request()
        request.a = a
        request.b = b 

        # async call
        future = self.client_.call_async(request)

        # ask ros to call response_callback when is future is complete
        future.add_done_callback(self.response_callback)
    
    def response_callback(self, future):
        try:
            response = future.result()
        except Exception as error:
            self.get_logger().error(f"Service call failed :{error}")
        else:
            self.get_logger().info(f"Sum: {response.sum}")
    
def main(args=None):
    rclpy.init(args=args)
    node = ServiceClient()

    try:
        # sending request from oridinary method 
        node.send_request(10.5,20.5)
        # keep the executor running so it can process the response
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()