from flask import Flask, flash, jsonify, redirect, render_template, request, session ,url_for
from flask_session import Session
import math
from helpers import login_required, hours_between_times
import cv2
import pickle
import numpy as np 
import time
import os
from database import new_schedule, update_password,update_username, get_user_details , get_license_no , hash_password  ,new_user,create_database,check_password_hash,get_user_details_by_id,check_schedule_reserve






app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


#Initalise Database



@app.route('/')
def index():
       if request.method == "GET":
            session.clear()
            if 'my_database.db' in os.listdir():
                pass
            else:
                create_database()
            return render_template("index.html")


shedule = []

@app.route('/home', methods=["GET", "POST"])
@login_required
def home():
    if request.method == "POST":
        id = session["user_id"]
        location = request.form.get("location")
        Date = request.form.get("Date")
        start_time = request.form.get("start-time")
        end_time = request.form.get("end-time")
        hours = hours_between_times(start_time,end_time)

        
        shedule.append([id,get_license_no(get_user_details_by_id(id)[1]),Date,start_time,end_time,math.floor(hours),location])
        print(shedule)
        
        return redirect("/reserve")
    else:
        return render_template('home.html')
      


  
        


@app.route('/reserve', methods=["GET","POST"])
@login_required
def reserve():

    if request.method == "POST":
        return redirect("/bill")
    else:
            
        start_time = time.time()

        width,height = 180, 170


        url ="http://192.168.101.5:8080/video"

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
                cv2.imshow(str(x*y),ImgCrop)
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
            
            cv2.imshow("imageBlur",imgBlur)
            
            parking_space(imgDilate)
            
            if not success:  # Check if the frame was captured successfully
                print("Error: Cannot capture frame")
                break
            
            if time.time() - start_time >= 3:
                break
            
            for pos in poslist:
                cv2.rectangle(img,(pos[0],pos[1]),(pos[0]+width,pos[1]+height),(255,0,255),2)
            cv2.namedWindow("Image", cv2.WINDOW_NORMAL)   
            cv2.imshow("Image",img)
            cv2.waitKey(1)
            
        cap.release()
        cv2.destroyAllWindows()
        # print(parking_box_id)
        def check_available_parking():
            unique_objects = []

            for obj in parking_box_id:
                if obj[2] not in unique_objects:
                    unique_objects.append(obj[2])

            return unique_objects
          
        print(check_available_parking())
        reserved_parking = []
        shedule_reserved_parking =  check_schedule_reserve(shedule[0][2],shedule[0][3],shedule[0][4])
        if  (shedule_reserved_parking):
            return render_template('reservation.html',parking_list=check_available_parking(),total_parking=poslist,reserved=reserved_parking)

        else:
            reserved_parking.append(shedule_reserved_parking)
            return render_template('reservation.html',parking_list=check_available_parking(),total_parking=poslist,reserved=reserved_parking,start_time=shedule_reserved_parking[1],end_time = shedule_reserved_parking[2])
            
            

            


@app.route("/login", methods=["GET", "POST"])
def login():
    
    session.clear()
 
    if request.method == "POST":
        print("fsdffsafsdaf")
        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("login.html", cerendiatals=False)
        

        # Ensure password was submitted
        elif not request.form.get("password"):
        
            return render_template("login.html",cerendiatals=False)

        # Query database for username
        user_details = get_user_details(request.form.get("username"))
        print(user_details)
        password = user_details[3]
        # Ensure username exists and password is correct
        if len(user_details) != 1 or check_password_hash(request.form.get("password"), password):        
            # Remember which user has logged in
            session["user_id"] = user_details[0]

            # Redirect user to home page
            return redirect("/home")
        else:
            print("chutyye")
            return render_template("login.html", cerendiatals=False)

    else:
        return render_template("login.html" , cerendiatals=True)
    
    
@app.route("/register",methods=["GET","POST"])
def register():
    """Register user"""

    # Forget any user_id
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password =request.form.get("password")
        email = request.form.get("email")
        car_no = request.form.get("car_no")
        confirm = request.form.get("confirm")
        mobile_no = request.form.get("mobile")
        
        print((password == confirm),password,confirm)

        if not username:
            return render_template("register.html", cerendiatals=False,password_match=True,username_taken=False)

        elif not password:
            return render_template("register.html",cerendiatals=False,password_match=True,username_taken=False)

        elif password != confirm:
            return render_template("register.html", password_match=False,cerendiatals=True,username_taken=False)
        
    
        
        
        user_details = get_user_details(username)
       
        if user_details == None:
            new_user(username,email,password,car_no,mobile_no)
        # redirect to login page
            return redirect("/home")

        
        return render_template("register.html", password_match=True,cerendiatals=True,username_taken=True)
        
       
        
    else:
        return render_template("register.html",cerendiatals=True,username_taken=False,password_match=True)
    
    
@app.route("/profile",methods=["GET","POST"])
@login_required
def profile():
    id = session["user_id"]
    
    
    if request.method == "POST":
        new_username = request.form.get("username")
        if update_username(id,new_username):
            return render_template("profile.html",username = get_user_details_by_id(id)[1],username_taken=False)
        else:
            return rendere_template("profile",username= get_user_details_by_id(id)[1],username_taken=True)
            
    else:
        return render_template("profile.html", username = get_user_details_by_id(id)[1],username_taken=False)

parking_slot = []

@app.route("/bill",  methods=["GET",'POST'])
def bill():
    
    if request.method == "POST":
        data = request.get_json()
        parking_slot.append(data['data'])
        shedule.append(data['data'][0])
        print(shedule)
        return jsonify({'message': 'Data received!'}), 200
    else:
        return render_template("billing.html",data=parking_slot[0])

@app.route("/pay",methods=["POST"])
def pay():
    new_schedule(shedule[0][0],shedule[0][1],shedule[0][2],shedule[0][3],shedule[0][4],shedule[0][5],shedule[0][6],int(shedule[1]))
    while len(shedule) != 0:
        shedule.pop()
        print(shedule)
    return render_template("thankyou.html")



if __name__ == '__main__':
    # data_thread = Thread(target=update_parking_data)
    # data_thread.start()
    # socketio.run(app, debug=True)
    app.run()
