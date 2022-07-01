import socket
import string
import cv2
import imutils
import time
import numpy
import sys
import base64
import os
import pickle
import threading

from pandas import StringDtype


class ClientSocket:
    def __init__(self, ip, port):
        self.TCP_SERVER_IP = ip
        self.TCP_SERVER_PORT = port
        self.connectCount = 0

        self.frame = None
        self.ret = None

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
            while True:

                    stringData = input()
                    length = str(len(stringData))
                    self.sock.sendall(length.encode('utf-8').ljust(64))
                    self.sock.send(stringData.encode('utf-8'))
                

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
    TCP_IP = '165.246.139.32'
    TCP_PORT = 9502
    client = ClientSocket(TCP_IP, TCP_PORT)

if __name__ == "__main__":
    main()
