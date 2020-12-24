import cv2
import numpy as np
from pyzbar.pyzbar import decode
import urllib.request


# img = cv2.imread('image.PNG')
cap = cv2.VideoCapture(0)
# cap = cv2.VideoCapture(1)
url= 'http://192.168.43.8/cam-lo.jpg'

# cap.open(url)
cap.set(3,640)
cap.set(4,480)
# for qrcode in decode(img):
#     print(qrcode)
# image = urllib.request.urlopen(url)
# print("IMage : ", image)
while True:
    # image = urllib.request.urlopen(url)
    success, img = cap.read()
    print("img :  ", img)
    # img = np.array(bytearray(image.read()),dtype=np.uint8)
    for qrcode in decode(img):
        # print(qrcode.data)
        myData = qrcode.data.decode('utf-8')
        print("mydata : ", myData)
        pts = np.array([qrcode.polygon],np.int32)
        pts = pts.reshape((-1,1,2))
        cv2.polylines(img,[pts],True,(255,0,255),5)

        pts2 = qrcode.rect
        cv2.putText(img,myData,(pts2[0],pts2[1]), cv2.FONT_HERSHEY_SIMPLEX,0.9,(255,0,255),2)
        

    cv2.imshow('Result : ', img)
    cv2.waitKey(1)
cap.release()

    # customer = request.user.customer
    # print("customer : ", customer)
    # customerqr, created = Customer_QR.objects.update_or_create(
    #         customer=customer, defaults={"items_json_qr": data}
#     #     )



# video = cv2.VideoCapture("http://192.168.43.8:81/stream")
# video = cv2.VideoCapture(1)


# while True:
#     _,frame = video.read()
#     cv2.imshow("RTSP", frame)
#     k = cv2.waitKey(1)
#     if k == ord('q'):
#         break
# video.release()
# cv2.destroyAllWindows()




