import socket
import cv2
import imutils
import time
import numpy
import sys
import base64
import os
import pickle
import threading


class ClientSocket:
    def __init__(self, ip, port):
        self.TCP_SERVER_IP = ip
        self.TCP_SERVER_PORT = port
        self.connectCount = 0

        self.frame = None
        self.ret = None

        self.updated = 0
        self.capture = cv2.VideoCapture(0)
        self.capture.set(cv2.CAP_PROP_FRAME_WIDTH, 720)
        self.capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)



        self.connectServer()
    def connectServer(self):
        try:
            self.sock = socket.socket()
            self.sock.connect((self.TCP_SERVER_IP, self.TCP_SERVER_PORT))
            print(u'Client socket is connected with Server socket [ TCP_SERVER_IP: ' + self.TCP_SERVER_IP + ', TCP_SERVER_PORT: ' + str(self.TCP_SERVER_PORT) + ' ]')
            self.connectCount = 0
            self.sendImages()
            
        except Exception as e:
            print(e)
            self.connectCount += 1
            if self.connectCount == 10:
                print(u'Connect fail %d times. exit program'%(self.connectCount))
                sys.exit()
            print(u'%d times try to connect with server'%(self.connectCount))
            self.connectServer()


    def sendImages(self):

        try:
            while self.capture.isOpened():
                    time_init = time.time()
                    self.ret, self.frame = self.capture.read()

                    resize_frame = cv2.resize(self.frame, dsize=(720, 480), interpolation=cv2.INTER_AREA)
                    encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),100]
                    result, imgencode = cv2.imencode('.jpg', resize_frame, encode_param)
                    data = numpy.array(imgencode)
                    stringData = base64.b64encode(data)


                    length = str(len(stringData))
                    self.sock.sendall(length.encode('utf-8').ljust(16))
                    self.sock.send(stringData)
                    time_finish = time.time()

                    print('FPS : %.2f'%(1/(time_finish-time_init)))

                

            raise

        

        except KeyboardInterrupt:
            self.sock.close()
            sys.exit() #종료

        except Exception as e:
            print(e)
            self.sock.close()
            time.sleep(1)
            self.connectServer()
            self.sendImages()

def main():
    TCP_IP = 'localhost'
    TCP_PORT = 8080
    client = ClientSocket(TCP_IP, TCP_PORT)

if __name__ == "__main__":
    main()