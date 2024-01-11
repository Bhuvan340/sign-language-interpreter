'''Data extraction code'''
import cv2
import numpy as np
import math
import time
from cvzone.HandTrackingModule import HandDetector
cam = cv2.VideoCapture(0)
detector = HandDetector(maxHands=1)
offset = 20
imgSize = 300

folder = "D:/Sign Language/Computer Vision/Data_ASL/No"
counter=112
try:
    while True:
        success, img = cam.read()
        hands, img = detector.findHands(img)
        if hands:
            hand = hands[0]
            x, y, w, h = hand['bbox']
    
            imgCrop = img[y-offset:y+h+offset, x-offset:x+w+offset]
            imgWhite = np.ones((imgSize, imgSize, 3), np.uint8)*255
            imgCropShape = imgCrop.shape
    
            aspectRatio = h/w
            if aspectRatio > 1:
                k = imgSize/h
                wCal = math.ceil(k*w)
                imgResize = cv2.resize(imgCrop, (wCal, imgSize))
                imgResizeShape = imgResize.shape
                wGap = math.ceil((imgSize-wCal)/2)
                imgWhite[:, wGap:wCal+wGap] = imgResize
            else:
                k = imgSize / w
                hCal = math.ceil(k * h)
                imgResize = cv2.resize(imgCrop, (imgSize, hCal))
                imgResizeShape = imgResize.shape
                hGap = math.ceil((imgSize - hCal) / 2)
                imgWhite[hGap:hCal + hGap, :] = imgResize
            cv2.imshow("ImageCrop", imgCrop)
            cv2.imshow("ImageCrop", imgWhite)
        cv2.imshow("Image", img)
        key = cv2.waitKey(1)
        if key == ord("s"):
            counter+=1
            cv2.imwrite(f'{folder}/Image_{time.time()}.jpg',imgWhite)
            print(counter)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    cam = cam.release()
    cv2.destroyAllWindows()
except Exception as e:
    print("Error:", e)
    cam = cam.release()
    cv2.destroyAllWindows()