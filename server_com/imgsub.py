import rospy
import numpy as np
from sensor_msgs.msg import CompressedImage
import cv2
rospy.init_node('img_receiver')

def callback(msg):
    img_byte = msg.data
    img_array = np.fromstring(img_byte,np.uint8)
    image = cv2.imdecode(img_array,1)
    print(image)

rospy.Subscriber('img',CompressedImage,callback)

while True:
    pass
