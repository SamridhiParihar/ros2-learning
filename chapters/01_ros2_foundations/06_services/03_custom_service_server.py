import rclpy
from rclpy.node import Node
from robot_interfaces.srv import AddTwoFloats

class ServiceServer(Node):

    def __init__(self):
        super().__init__("service_server_node")

        # creating service 
        self.service_ = self.create_service(
            AddTwoFloats,
            "/add_two_floats",
            self.add_two_floats
        )
        self.get_logger().info('Service Server Node has been started.')

    
    def add_two_floats(self, request,response):
        self.get_logger().info(f"Service server add_two_floats started with request as; a: {request.a} , b :{request.b}")
        a = request.a
        b = request.b 
        result = a+b
        response.sum = result
        self.get_logger().info(f"Service server add_two_floats finished with response sum as : {response.sum}")

        return response 

def main(args=None):
    rclpy.init(args=args)
    node = ServiceServer()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
