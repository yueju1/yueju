
import time

import rclpy
from rclpy.node import Node

class Imag(Node):

    # if asd.ImageSubscriber().ok == 1:

    #     print(s.AutoCalibration().m)
    def __init__(self):
        #这里面的不报位置吗     
        super().__init__('image_detecn')
        self.declare_parameter('asd',1)


def main():
    rclpy.init()
    image_subscriber = Imag()

    rclpy.spin(image_subscriber)
    image_subscriber.destroy_node()
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()