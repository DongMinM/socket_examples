# -*- coding:utf-8 -*-

import socket
import cv2
from cv2 import IMWRITE_JPEG_CHROMA_QUALITY
import numpy as np
import threading
import time
import base64

import rospy
from sensor_msgs.msg import CompressedImage

# 참고1 https://walkinpcm.blogspot.com/2016/05/python-python-opencv-tcp-socket-image.html
# https://millo-l.github.io/Python-TCP-image-socket-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0-Server-Client/

'''  
thread 1 : wait client
thread 2 : receive datas
thread 3 : show image
'''



class ServerSocket:

    def __init__(self, ip, port):
        ## server ip and port
        self.TCP_IP = ip
        self.TCP_PORT = port

        self.img_update = 0
        self.img_client = 0

        rospy.init_node('server')
        self.pub2js = rospy.Publisher('img',CompressedImage,queue_size=1)

        # thread for showing Opencv image
        self.thread_img = threading.Thread(target = self.img_pub)
        self.thread_img.start()

        ## server socket open ( start )
        self.thread_recv = threading.Thread(target = self.socketOpen)
        self.thread_recv.start()




    ## close server socket
    def socketClose(self):
        self.sock.close()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is closed')

    ## open server socket
    def socketOpen(self):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)           # server socket
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)         # server socket option
        self.sock.bind((self.TCP_IP, self.TCP_PORT))                            # server socket bind
        self.sock.listen(2)                                                     # number of client can be access at the same time (but not work for this code)
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is opened')

        # accept every client, any time
        while True:
            client_socket, addr = self.sock.accept()
            print('접속 : ',(addr))

            # thread that receive datas
            threading.Thread(target=self.receivedatas, args =(client_socket,addr)).start()


    ## show opencv image
    def img_pub(self):
        while True:
            if self.img_update == 1:
                msg = CompressedImage()
                msg.format = 'jpeg'
                msg.data = np.array(cv2.imencode('.jpg', self.decimg)[1]).tostring()
                self.pub2js.publish(msg)
            else:
                pass


    ## receive data from client socket
    def receivedatas(self,client_socket,addr):
        try:
            while True:

                time_init = time.time()
                length = self.recvall(client_socket, 64)
                stringData = self.recvall(client_socket, int(length))

                if stringData[0] == 115:

                        if stringData.decode('utf8') == 'stop':
                            print('stop')
                            raise
                        else:
                            print(stringData.decode('utf8'))

                else:

                        data = np.frombuffer(base64.b64decode(stringData), dtype='uint8')
                        self.decimg = cv2.imdecode(data, 1)
                        self.img_update = 1
                        self.img_client = addr
                        # print(self.decimg)
                        time_finish = time.time()
                        #print('FPS : %.1f'%(1/(time_finish-time_init)))



        ## exception / client is out
        except Exception as e:
                print(e)
                ## if img_client is out, stop img_show
                if addr == self.img_client:
                    self.img_update = 0
                print('접속 종료 : ',(addr))
                time.sleep(1)



    ## recv all data (client socket, data count)
    def recvall(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf


# 9502 -> 8080
if __name__ == "__main__":
    server = ServerSocket('192.168.0.37', 8080)
    

