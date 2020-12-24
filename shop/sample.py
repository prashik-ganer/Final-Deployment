import cv2
from pyzbar.pyzbar import decode
import numpy as np
import urllib.request
import time
import requests
import io

url = 'http://192.168.43.8/cam-lo.jpg'
cv2.namedWindow("window", cv2.WINDOW_AUTOSIZE)

while True:
    imgResponse = urllib.request.urlopen(url)
    imgnp = np.array(bytearray(imgResponse.read()), dtype=np.uint8)
    # print("imgnp  :  ",imgnp)
    img = cv2.imdecode(imgnp, -1)
    print(img)

    # print("img : ", img)
    for qrcode in decode(img):
        # print(qrcode.data)
        myData = qrcode.data.decode('utf-8')
        print("mydata : ", myData)
        file1 = open('sample.txt','a')
        file1.write(myData)
        file1.write("\n")
        pts = np.array([qrcode.polygon],np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(img,[pts],True,(204,102,0),5)

        pts2 = qrcode.rect
        cv2.putText(img,myData,(pts2[0],pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,0.9,(204,102,0),2)
    # gray = cv2.cvtColor(img, cv2.COLOR_BayerBG2GRAY)

    cv2.imshow("window", img)
    # while True:
    image_url = "local-"+ str(time.time()) +"filenamk.jpg"
    image = urllib.request.urlretrieve(url, image_url)
    data = open(image_url,'rb').read()
    # index = open("http://iottransporter.com/IoT/project/chain_snatcher/prashik/index.py",'w')
    requests.post("http://iottransporter.com/IoT/project/chain_snatcher/prashik/index.py",data=data)
    # requests.post("https://iottransporter.com/IoT/project/chain_snatcher/prashik/index.py", files=image)
    key = cv2.waitKey(5000)
    if key == ord('q'):
        break

cv2.destroyAllWindows



# cap = cv2.VideoCapture('http://192.168.43.8')

# currentFrame=0
# while(True):
#     ret, frame = cap.read()

#     frame = cv2.flip(frame,1)

#     gray = cv2.cvtColor(frame, cv2.COLOR_BayerBG2GRAY)

#     cv2.imshow('frame', gray)
#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break

#     currentFrame += 1

# cap.release()
# cv2.destroyAllWindows()