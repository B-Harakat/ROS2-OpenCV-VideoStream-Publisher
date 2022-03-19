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


# Capture one frame from camera and returning the image.
def camera_capture():

    ret, frame = cam.read()
    frame = cv2.resize(frame,(960,640))

    return frame

class Opencv_Publisher(Node):
 
    def __init__(self):
        super().__init__('opencv_publisher')
      
        self.publisher_ = self.create_publisher(Image, 'rgb_cam/image_raw', 10)

        self.bridge = CvBridge()
        fps = 30
        timer_period = 1/fps  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

   
 
    def timer_callback(self):

        img = camera_capture()
   
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



