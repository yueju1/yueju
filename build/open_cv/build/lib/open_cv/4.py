from typing import List
import cv2
from rcl_interfaces.msg import SetParametersResult
import rclpy
from rclpy.node import Node
from rclpy.parameter import Parameter
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
from control_msgs.msg import JointControllerState


class ImageSubscriber(Node):

    def __init__(self):

        super().__init__('image_detection')
        
        self.subscription = self.create_subscription(
            Image,
            '/Cam2/image_raw',
            self.listener_callback,
            10)
        
        self.sub2 = self.create_subscription(JointControllerState,'/joint_trajectory_controller/state',
                                             self.state_callback,10)

        self.subscription  # prevent unused variable warning

        self.br = CvBridge()
    # is the callbackfunction a must?

    def state_callback(self,msg):
        self.get_logger().info('%s' % msg.joint_names)
        print(msg.joint_names)

    def listener_callback(self, data):

        im = self.br.imgmsg_to_cv2(data)
        
        # im = cv2.imread("/home/pmlab/yueju3/robot/Greifer_Unterseitenkamera.bmp")    
        # gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)    
        gray2 = cv2.GaussianBlur(im, (3, 3),1)
        # gray2 = cv2.medianBlur(im, 5)
        canny = cv2.Canny(gray2, 55, 230) # , apertureSize = 3)
        _, thresh = cv2.threshold(canny, 140, 220, cv2.THRESH_BINARY)  
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  
            #最小二乘法拟合椭圆  椭圆检测能检测圆吗 摄像机侧边拍真的是椭圆吗（不倾斜，相互平行）
            # 检测椭圆内圈？
        ( 1070.2332763671875, 563.084716796875, 120.31209564208984, 127.44139099121094)
        for i in contours:  #sobel? kaolv geng fuza yidian
            if len(i) >= 5 :
                retval = cv2.fitEllipse(i)  
                cv2.ellipse(im, retval, (0, 0, 255), thickness=1) 
                cv2.circle(im, (int(retval[0][0]),int(retval[0][1])),3, (0, 0, 255), -2)
                
                col = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)
                cv2.drawContours(col, contours, -1, (0, 0, 255), 1)
             
                print(retval) 
            # 还有别的方法画椭圆中心吗
        cv2.namedWindow('ellip',0)
        cv2.resizeWindow('ellip',1000,1000)
        cv2.imshow("ellip", im)

        cv2.namedWindow('ellips',0)
        cv2.resizeWindow('ellips',1000,1000)
        cv2.imshow("ellips", canny)
        
        cv2.waitKey(1)


def main():
    rclpy.init()
    image_subscriber = ImageSubscriber()

    rclpy.spin(image_subscriber)
    image_subscriber.destroy_node()
    rclpy.shutdown()
 
if __name__ == "__main__":
    main()