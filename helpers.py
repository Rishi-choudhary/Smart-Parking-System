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


# from camera import parking_space


# def apology(message, code=400):
#     """Render message as an apology to user."""
#     def escape(s):
    
#         for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
#                          ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
#             s = s.replace(old, new)
#         return s
#     return render_template("apology.html", top=code, bottom=escape(message)), code


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

    return hours

def generate_frames():
    url= "http://192.168.101.9:8080/video"

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

        width,height = 180, 170


        url= "http://192.168.101.9:8080/video"

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

        
    
    
    

# def check_schedule_reserve(date,start_time,end_time,location):
#     conn = sqlite3.connect('my_database.db')
#     cursor = conn.cursor()

#     # Check if another user already has the same username
#     cursor.execute("SELECT * FROM shedule WHERE location = ? and date_added = ?", (location,date,))
#     parking_shedules = cursor.fetchall()
#     start_time  = int(start_time[:2])
#     end_time  =  int(end_time[:2])
#     print(start_time,end_time)
#     parkings = []
#     for parking in parking_shedules:
#         if (start_time - parking[3]) > 0 and (start_time - parking[4]) < 0:
#             parkings.append(int(parking[7]))
            
#         # elif (start_time - parking[3]) > 0 and (end_time - parking[4]) > 0:
#         #     return True
#         elif (start_time - parking[3]) < 0 and (end_time - parking[4]) > 0:
#             parkings.append(int(parking[7]))
#             print("parking")
#         else:
#             return True
        
#     return parkings
        


    
    
def calculate_similarity(list1, list2):
    set1 = set(list1)
    set2 = set(list2)

    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))

    similarity_percentage = (intersection / union) * 100
    return similarity_percentage


# import serial
# import cv2
# import numpy as np
# import requests

# ser = serial.Serial('COM3', 115200)  # Change 'COM3' to your Arduino's serial port
# url = 'http://127.0.0.1:5000/capture'  # Adjust the Flask server URL

# def send_to_flask(data):
#     response = requests.post(url, data=data)
#     print(response.text)

# def process_image(image_data):
#     # Reconstruct the image from the received data
#     image_array = np.frombuffer(image_data, dtype=np.uint8)
#     image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)

#     # Perform image processing or analysis as needed
#     # Example: Convert to grayscale
#     gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#     # Example: Display the images
#     cv2.imshow('Original Image', image)
#     cv2.imshow('Grayscale Image', gray_image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

# while True:
#     if ser.in_waiting > 0:
#         signal = ser.readline().decode().strip()
#         if signal == '1':
#             # Read entire image data as a single block
#             camera_data = ser.read(320 * 240)  # Adjust based on your image size

#             # Send camera data to Flask
#             send_to_flask(camera_data)

#             # Process the image using OpenCV
#             process_image(camera_data)
