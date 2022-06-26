import rospy
from std_msgs.msg import Float32MultiArray
import cv2
import numpy as np
import base64

class Imager():

    def __init__(self):
        rospy.init_node('shower')
        rospy.Subscriber('img', Float32MultiArray, self.imgshow)
        rospy.spin()

    def imgshow(self,msg):
        img = np.array(msg.data)
        stringData = base64.b64encode(img)
        data = np.frombuffer(base64.b64decode(stringData), dtype='uint8')
        print(data)
        # msg = np.array(msg.data)
        # print(msg.)
        # self.img = base64.b64encode(msg)
        # # print(self.img)
        # data = np.frombuffer(self.img, dtype='uint8')
        # print(data)
        # image = cv2.imdecode(img, 1)
        # print(image)
        cv2.imshow('image',data)
        

        cv2.waitKey(1)


if __name__ == '__main__':
    shower = Imager()
