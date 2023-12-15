import cv2
import pickle

url ="http://192.168.101.4:8080/video"


cap = cv2.VideoCapture(url)

width,height = 100, 100

try:
    with open('CarParkPos',"rb") as f:
        poslist = pickle.load(f)
        print(poslist)
except:
    poslist = []
    

def mouseClick(events,x,y, flags, params):
    if events == cv2.EVENT_LBUTTONDOWN:
        box_id = len(poslist) + 1
        poslist.append((x,y,box_id))
    if events == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(poslist):
            x1,y1,box_id = pos
            if x1 < x < x1+width and y1 < y < y1+height:
                print(f"Removed box {box_id}")
                poslist.pop(i)
                

    with open('CarParkPos',"wb") as f:
        pickle.dump(poslist,f) 
        
                   
    
    
    

while True:
    success,image = cap.read()
    
    for pos in poslist:
        cv2.rectangle(image,(pos[0],pos[1]),(pos[0]+width,pos[1]+height),(255,0,255),2)        
    # # Inside your detection loop
    # for pos in poslist:
    #     x, y, box_id = cv2.boundingRect(pos)
    cv2.namedWindow("Image", cv2.WINDOW_NORMAL)   
    cv2.imshow("Image",image)

    cv2.setMouseCallback("Image",mouseClick)
    cv2.waitKey(1)
    