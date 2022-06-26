import cv2

img = cv2.imread("/dev/video0")

print(type(img))
# numpy.ndarray

print(img.shape)