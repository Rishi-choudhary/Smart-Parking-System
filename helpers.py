from flask import redirect, render_template, session
import json
from functools import wraps
from datetime import datetime
import cv2
import pickle
import numpy as np 
import time
import os
from database import *



def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function

def admin_login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("admin_id") is None:
            return redirect("/adminLogin")
        return f(*args, **kwargs)
    return decorated_function


def hours_between_times(start_time, end_time):
    # Define the time format for 24-hour clock (e.g., "HH:MM")
    time_format = "%H:%M"

    # Parse the start and end times
    start_time_obj = datetime.strptime(start_time, time_format)
    end_time_obj = datetime.strptime(end_time, time_format)

    # Calculate the time difference in hours
    time_difference = end_time_obj - start_time_obj

    # Extract the number of hours from the time difference
    hours = time_difference.total_seconds() / 3600

    if hours < 0 :
        return (12 + abs(hours))
    else:
        return hours

def generate_frames():
    
    url = "https://192.168.101.4:8080/video"
    camera = cv2.VideoCapture(url)
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                 b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def reserve_function(date):
              
    current_date = datetime.now()

    # Format the date as dd-mm-yy
    formatted_date = current_date.strftime("%y-%m-%d")
    print(formatted_date)
    if date == formatted_date:
        start_time = time.time()

        
        width,height = 100 , 100


        url = "https://192.168.251.222:8080/video"


        #video Feed
        cap = cv2.VideoCapture(url)

        with open('CarParkPos',"rb") as f:
                poslist = pickle.load(f)
        
        
        parking_box_id = []
        
        def parking_space(imgPro):
            for pos in poslist:
                x = pos[0]
                y = pos[1]
                ImgCrop = imgPro[y:y+height,x:x+height]
                count = cv2.countNonZero(ImgCrop)
                if count<800:
                    color = (0,255,0)
                    thickness =5
                    parking_box_id.append(pos)
                    
                else:
                    thickness =2
                    color = (0,0,255)
                cv2.rectangle(img,(pos[0],pos[1]),(pos[0]+width,pos[1]+height),color,thickness)
                
        
        
        while True:
            success,img = cap.read()
            
            imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            imgBlur = cv2.GaussianBlur(imgGray,(3,3),1)
            
            imgThreshold = cv2.adaptiveThreshold(imgBlur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV,25,16)
            imgMedian = cv2.medianBlur(imgThreshold,5)
            kernel = np.ones((3,3),np.uint8)
            imgDilate = cv2.dilate(imgMedian,kernel,iterations=1)
            
            
            parking_space(imgDilate)
            
            if not success:  # Check if the frame was captured successfully
                print("Error: Cannot capture frame")
                break
            
            if time.time() - start_time >= 2:
                break
            
            for pos in poslist:
                cv2.rectangle(img,(pos[0],pos[1]),(pos[0]+width,pos[1]+height),(255,0,255),2)
            cv2.waitKey(1)
            
        cap.release()
        cv2.destroyAllWindows()
        # print(parking_box_id)
        unique_objects = []

        for obj in parking_box_id:
            if obj[2] not in unique_objects:
                unique_objects.append(obj[2])

        return unique_objects
    else:
        reserved = []
        conn = sqlite3.connect('my_database.db')
        cursor = conn.cursor()
        cursor.execute('''
        SELECT * FROM Schedule
        WHERE date_added = ?
    ''', (date,))
        parking_list = cursor.fetchall()
   
        for parking in parking_list: 
            reserved.append(parking[7])
        conn.close()
        return reserved

        
    
    
    

        


    