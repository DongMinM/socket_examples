import socket
import cv2
import numpy
import threading
import time
import base64
import rospy
from std_msgs.msg import Float32MultiArray

# 참고1 https://walkinpcm.blogspot.com/2016/05/python-python-opencv-tcp-socket-image.html
# https://millo-l.github.io/Python-TCP-image-socket-%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0-Server-Client/

class ServerSocket:

    def __init__(self, ip, port):
        self.TCP_IP = ip
        self.TCP_PORT = port

        self.socketOpen()
        self.receiveThread = threading.Thread(target=self.receiveImages)
        self.receiveThread.start()


    def socketClose(self):
        self.sock.close()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is close')

    def socketOpen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.TCP_IP, self.TCP_PORT))
        self.sock.listen(1)
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is open')
        self.conn, self.addr = self.sock.accept()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is connected with client')

    def receiveImages(self):
        while True:
            try:

                time_init = time.time()
                length = self.recvall(self.conn, 16)
                if length is not None:
                    stringData = self.recvall(self.conn, int(length))
                    tt2 = time.time()
                    # print(sys.getsizeof(stringData))

                    data = numpy.frombuffer(base64.b64decode(stringData), dtype='uint8')
                    decimg = cv2.imdecode(data, 1)


                    # 이미지 크기 확인
                    # cv2.imwrite("123123.jpg",decimg)
                    # print(os.path.getsize('123123.jpg'))


                    cv2.imshow("image", decimg)
                    cv2.waitKey(1)

                    time_finish = time.time()
                    print('FPS : %.1f'%(1/(time_finish-time_init)))

                else :
                    raise
                

            except Exception as e:
                print(e)
                cv2.destroyAllWindows()
                self.socketClose()
                self.socketOpen()


    def recvall(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

def main():
    server = ServerSocket('localhost', 8080)

if __name__ == "__main__":
    main()