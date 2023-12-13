from flask import Flask, flash, jsonify, redirect, render_template, request, session ,url_for,Response
from flask_session import Session
import math
from helpers import *
import pickle
import os
import sqlite3
import hashlib
from sqlite3 import Error
from datetime import datetime
from database import *




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

current_date = datetime.now()

# Format the date as dd-mm-yy
formatted_date = current_date.strftime("%y-%m-%d")

@app.route('/home', methods=["GET", "POST"])
@login_required
def home():
    locationsList = ["SILVASSA", "VAPI"];
    
    if request.method == "POST":
        id = session["user_id"]
        location = request.form.get("location")
        date = request.form.get("Date")
        print(date)
        start_time = request.form.get("start-time")
       
        end_time = request.form.get("end-time")
        hours = hours_between_times(start_time,end_time)

        if location not in locationsList:
            return render_template("home.html", location=False)
        
        shedule.append([id,get_license_no(get_user_details_by_id(id)[1]),date,start_time,end_time,math.floor(hours),location])
        print(shedule)
        
        return redirect("/reserve")
    else:
        while len(shedule) != 0:
            shedule.pop()
        return render_template('home.html',location=True)
      


  
        


@app.route('/reserve', methods=["GET","POST"])
@login_required
def reserve():
    
    with open('CarParkPos',"rb") as f:
            poslist = pickle.load(f)
    

    if request.method == "POST":
        return redirect("/bill")
    else:
        date = shedule[0][2]
        start_time = shedule[0][3]
        end_time =shedule[0][4]
        reserve_fucntion_list = reserve_function(formatted_date)
       
        reserved = check_reservation(date,start_time,end_time,shedule[0][6])
        
        # if check_schedule_reserve(shedule[0][2],shedule[0][3],shedule[0][4]):
        #     pass
        #     print("moye moye")
        # else:
        #     shedule_reserved_parking.append(int((check_schedule_reserve(shedule[0][2],shedule[0][3],shedule[0][4]))))
        #     print(shedule_reserved_parking)

        return render_template('reservation.html',parking_list=reserve_fucntion_list,total_parking=poslist,reserved=reserved)

        
            

            
            


@app.route("/login", methods=["GET", "POST"])
def login():
    
    session.clear()
 
        
        
    if request.method == "POST":
        

        if not request.form.get("username") or not request.form.get("password"):
            return render_template("login.html", credentials=False)

        # Query database for admin details
        user_details = get_user_details(request.form.get("username"))
        if len(user_details) == 0 :
            return render_template("login.html", credentials=False)
        
        password = user_details[0][3]
        

        # Ensure admin details exist and password is correct
        if check_password_hash(request.form.get("password"), password):        
            # Remember which user has logged in
            session["user_id"] = user_details[0][0]

            # Redirect user to home page
            return redirect("/home")
        else:
            return render_template("login.html", cerendiatals=False)
        # # Ensure username was submitted
        # if not request.form.get("username"):
        #     return render_template("login.html", cerendiatals=False)
        

        # # Ensure password was submitted
        # elif not request.form.get("password"):
        
        #     return render_template("login.html",cerendiatals=False)

        # # Query database for username
        # user_details = get_user_details(request.form.get("username"))
        # print(user_details)
        # password = user_details[3]
        # # Ensure username exists and password is correct
        # if len(user_details) != 1 or check_password_hash(request.form.get("password"), password):        
        #     # Remember which user has logged in
        #     session["user_id"] = user_details[0]

        #     # Redirect user to home page
        #     return redirect("/home")
        # else:
        #     print("chutyye")
        #     return render_template("login.html", cerendiatals=False)

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
        
        if len(user_details) == 0 :
            new_user(username,email,password,car_no,mobile_no)
            return redirect("/home")
            
       
        return render_template("register.html", password_match=True,cerendiatals=True,username_taken=True)
        
       
        
    else:
        return render_template("register.html",cerendiatals=True,username_taken=False,password_match=True)
    
    
    
    
@app.route("/adminLogin",methods=["GET","POST"])
def admin_login():
    session.clear()
    

    if request.method == "POST":
        if not request.form.get("username") or not request.form.get("password"):
            return render_template("adminLogin.html", credentials=False)

        # Query database for admin details
        admin_details = get_admin_details( request.form.get("username"))
        if len(admin_details) == 0:
            print("not nuser")
            return render_template("adminLogin.html", credentials=False)
        
        password = admin_details[0][2]
        print("fsfs")
        # Ensure admin details exist and password is correct
        if check_password_hash(request.form.get("password"), password):                    
            session["admin_id"] = admin_details[0][0]
            print("risisfs")
            # Redirect admin to the home page
            return redirect("/admin")
        else:
            return render_template("adminLogin.html", credentials=False)


    else:
        return render_template("adminLogin.html" , cerendiatals=True)



@app.route("/admin")
@admin_login_required
def admin():
    id = session["admin_id"]
    
    with open('CarParkPos',"rb") as f:
        poslist = pickle.load(f)
    reserve_fucntion_list = len(reserve_function(formatted_date))
    
    admin_location = get_admin_details_by_id(id)[0][4]  
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Schedule WHERE location = ?", (admin_location,))
    locations = cursor.fetchall()
    conn.close()
    return render_template("dashboard.html",admin=True,locations=locations,parking_list=reserve_fucntion_list,total_parking=len(poslist))

@app.route("/admin/reserved")
@admin_login_required
def reserved():
    
    
      
    with open('CarParkPos',"rb") as f:
        poslist = pickle.load(f)
    reserve_fucntion_list = reserve_function(formatted_date)
    return render_template('reserved.html',parking_list=reserve_fucntion_list,total_parking=poslist,admin=True)
    
@app.route("/admin/view_parking")
@admin_login_required
def view_parking():
    return render_template("view_parking.html",admin=True)

@app.route("/admin/pricing",methods=["GET","POST"])
@admin_login_required
def pricing():
    id = session['admin_id'] 
    
    if request.method == "POST":
        price = request.form.get("price")
        print(type(price))
        if update_admin_location_price(id,int(price)):
            return render_template("pricing.html",admin=True,show_message=True,price = get_admin_details_by_id(id)[0][5])
        return "SOMETHING ERROR OCCURRED"
    return render_template("pricing.html",admin=True,price = get_admin_details_by_id(id)[0][5])
        
        

@app.route("/admin/history")
@admin_login_required
def history():
    id = session["admin_id"]
    admin_location = get_admin_details_by_id(id)[0][4]
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Schedule WHERE location = ?", (admin_location,))
    locations = cursor.fetchall()
    conn.close()
    return render_template("history.html",admin=True,locations=locations)

@app.route("/admin/profile",methods=["GET","POST"])
@admin_login_required
def admin_profile():
    id = session["admin_id"]
    admin_details = get_admin_details_by_id(id)[0]
    print(admin_details)
    location = admin_details[4]
    if request.method == "POST":
        new_username = request.form.get("username")
        if update_admin_username(id,new_username):
            return render_template("adminProfile.html",username =admin_details[1],username_taken=False,location=location,admin=True)
        else:
            return rendere_template("adminProfile.html",username=admin_details[1],username_taken=True,location=locatio,admin=Truen)
            
    else:
        return render_template("adminProfile.html", username=admin_details[1],username_taken=False,location=location,admin=True)
    return render_template("adminProfile.html",location=location,admin=True)




    
@app.route("/profile",methods=["GET","POST"])
@login_required
def profile():
    id = session["user_id"]
    
    
    if request.method == "POST":
        new_username = request.form.get("username")
        if update_username(id,new_username):
            return render_template("profile.html",username = get_user_details_by_id(id)[1]
                                   ,username_taken=Fa13lse)
        else:
            return rendere_template("profile",username= get_user_details_by_id(id)[1],username_taken=True)
            
    else:
        return render_template("profile.html", username = get_user_details_by_id(id)[1],username_taken=False)

parking_slot = []

@app.route("/bill",  methods=["GET",'POST'])
@login_required
def bill():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin WHERE location = ?", (shedule[0][6],))
    admin_details = cursor.fetchall()
    conn.close()
    if request.method == "POST":
        data = request.get_json()
        parking_slot.append(data['data'])
        shedule.append(data['data'][0])
        print(shedule)
        return jsonify({'message': 'Data received!'}), 200
    
    else:
        print(parking_slot)
        return render_template("billing.html",data=parking_slot[0],price=admin_details[0][5],hours=hours_between_times(shedule[0][3],shedule[0][4]),date=shedule[0][2])

@app.route("/pay",methods=["POST"])
@login_required
def pay():
    new_schedule(shedule[0][0],shedule[0][1],shedule[0][2],shedule[0][3],shedule[0][4],shedule[0][5],shedule[0][6],int(shedule[1]))
    while len(shedule) != 0:
        shedule.pop()
        print(shedule)
    return render_template("thankyou.html")

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


if __name__ == '__main__':
    # data_thread = Thread(target=update_parking_data)
    # data_thread.start()
    # socketio.run(app, debug=True)
    app.run()
