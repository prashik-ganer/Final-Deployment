import cv2
import numpy as np
from pyzbar.pyzbar import decode
import urllib.request

import requests
import json


# url= 'http://127.0.0.1:8000/shop/scan/'
# cv2.namedWindow("Window", cv2.WINDOW_AUTOSIZE)

video_capture = cv2.VideoCapture(0)


while True:
    image = video_capture.read()
    imgnp = np.array(bytearray(image.read()),dtype=np.uint8)
    img = cv2.imdecode(imgnp, -1)
    for qrcode in decode(img):
        myData = qrcode.data.decode('utf-8')
        print("mydata : ", myData)
        
        pts = np.array([qrcode.polygon],np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(img,[pts],True,(51,255,255),5)
        pts2 = qrcode.rect
        cv2.putText(img,myData,(pts2[0],pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,0.9,(51,255,255),2)
    cv2.imshow('Result : ', img)
    cv2.waitKey(1)
cap.release()