#!/usr/bin/env python
from __future__ import print_function



import sys
import rclpy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
from rclpy.node import Node



cam = cv2.VideoCapture(0)




# while True:
#     camera_capture()

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break


# cam.release()
# # Destroy all the windows
# cv2.destroyAllWindows()

def camera_capture():


    ret, frame = cam.read()
    frame = cv2.resize(frame,(960,640))


    return frame

class Opencv_Publisher(Node):
 
    def __init__(self):
        super().__init__('opencv_publisher')
        # self.image_pub = r.Publisher("image_topic_2",Image)
        self.publisher_ = self.create_publisher(Image, 'rgb_cam/image_raw', 10)

        self.bridge = CvBridge()
        fps = 30
        timer_period = 1/fps  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        # self.image_sub = rospy.Subscriber("topic",Image,self.callback)
 
    def timer_callback(self):
        # try:
        #     cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        # except CvBridgeError as e:
        #     print(e)
  
        # (rows,cols,channels) = cv_image.shape
        # if cols > 60 and rows > 60 :
        #     cv2.circle(cv_image, (50,50), 10, 255)
 
        # cv2.imshow("Image window", cv_image)
        # cv2.waitKey(3)

        img = camera_capture()

        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     pass
   
        try:
            self.publisher_.publish(self.bridge.cv2_to_imgmsg(img, "bgr8"))
        except CvBridgeError as e:
            print(e)
   

def main(args=None):

    rclpy.init(args = args)
    opencv_publisher = Opencv_Publisher()

    try:
        rclpy.spin(opencv_publisher)
    except KeyboardInterrupt:
        print("Shutting down")

    cam.release()        
    cv2.destroyAllWindows()
   
if __name__ == '__main__':
    main()



# class MinimalPublisher(Node):

#     def __init__(self):
#         super().__init__('minimal_publisher')
#         self.publisher_ = self.create_publisher(String, 'topic', 10)
        # timer_period = 0.5  # seconds
        # self.timer = self.create_timer(timer_period, self.timer_callback)
        # self.i = 0

#     def timer_callback(self):
#         msg = String()
#         msg.data = 'Hello World: %d' % self.i
#         self.publisher_.publish(msg)
#         self.get_logger().info('Publishing: "%s"' % msg.data)
#         self.i += 1


# def main(args=None):
#     rclpy.init(args=args)

#     minimal_publisher = MinimalPublisher()

#     rclpy.spin(minimal_publisher)

#     # Destroy the node explicitly
#     # (optional - otherwise it will be done automatically
#     # when the garbage collector destroys the node object)
#     minimal_publisher.destroy_node()
#     rclpy.shutdown()


# if __name__ == '__main__':
#     main()