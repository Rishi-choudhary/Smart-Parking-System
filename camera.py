import cv2
import pickle
import cvzone
import numpy as np 
import time


width,height = 210, 210


def camera_feed():
    url ="http://192.168.101.9:8080/video"

    #video Feed
    cap = cv2.VideoCapture(url)

    with open('CarParkPos',"rb") as f:
            poslist = pickle.load(f)

    def parking_space(imgPro):
        data = []
        for pos in poslist:
            x = pos[0]
            y = pos[1]
            
            
            ImgCrop = imgPro[y:y+height,x:x+height]
            cv2.imshow(str(x*y),ImgCrop)
            count = cv2.countNonZero(ImgCrop)
            if count<800:
                color = (0,255,0)
                thickness =5
                
            else:
                thickness =2
                color = (0,0,255)
                data+=pos
                
            cv2.rectangle(img,(pos[0],pos[1]),(pos[0]+width,pos[1]+height),color,thickness)
        print(data)
        


    while True:
        success,img = cap.read()
        
        imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)
        
        imgThreshold = cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
        imgMedian = cv2.medianBlur(imgThreshold,5)
        kernel = np.ones((3,3),np.uint8)
        imgDilate = cv2.dilate(imgMedian,kernel,iterations=1)
        
        cv2.imshow("imageBlur",imgBlur)
        
        parking_space(imgDilate)
        for pos in poslist:
            cv2.rectangle(img,(pos[0],pos[1]),(pos[0]+width,pos[1]+height),(255,0,255),2)
        # cv2.resize(img, (900, 800))  
        cv2.namedWindow("Image", cv2.WINDOW_NORMAL)   
        cv2.imshow("Image",img)
        cv2.waitKey(1)
        
        
camera_feed()