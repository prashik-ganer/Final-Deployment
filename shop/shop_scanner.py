import cv2
import numpy as np
from pyzbar.pyzbar import decode
import urllib.request



# def scanqr():
url= 'http://192.168.43.8/cam-lo.jpg'
cv2.namedWindow("Window", cv2.WINDOW_AUTOSIZE)

while True:
    image = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(image.read()),dtype=np.uint8)
    img = cv2.imdecode(imgnp, -1)
    for qrcode in decode(img):
        myData = qrcode.data.decode('utf-8')
        print("mydata : ", myData)
        file1 = open('sample.txt','a')
        file1.write(myData)         
        file1.write("\n") 
        pts = np.array([qrcode.polygon],np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(img,[pts],True,(51,255,255),5)
        pts2 = qrcode.rect
        cv2.putText(img,myData,(pts2[0],pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,0.9,(51,255,255),2)
    cv2.imshow('Result : ', img)
    cv2.waitKey(1)
cap.release()