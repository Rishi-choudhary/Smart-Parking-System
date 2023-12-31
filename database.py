import sqlite3
import hashlib
import random
from sqlite3 import Error


def create_database():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    print("created Database")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS User (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            car_no TEXT,
            mobile_no TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Schedule (
            id INTEGER ,
            car_no TEXT,
            date_added DATE,
            start_time TIME,
            end_time TIME,
            hours INT,
            location TEXT,
            parking_slot INT
        )
    ''')
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        email TEXT NOT NULL,
        location TEXT NOT NULL,
        price INT NOT NULL
        )
    """)
    cursor.execute("""
CREATE TABLE IF NOT EXISTS parkings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    parking_slot TEXT NOT NULL,
    location TEXT NOT NULL,
    price REAL NOT NULL,
    car_license_no TEXT NOT NULL,
    parking_id INT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
                   """)
    conn.commit()
    conn.close()

def hash_password(password):
    # Hash the password before storing it in the database
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_details(username):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE username = ?", (username,))
    user = cursor.fetchall()
    conn.close()
    return user

def update_username(user_id, new_username):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    # Check if another user already has the same username
    cursor.execute("SELECT id FROM User WHERE username = ? AND id != ?", (new_username, user_id))
    existing_user_id = cursor.fetchone()

    if existing_user_id:
        conn.close()
        return False
    else:
        # Update the username
        cursor.execute("UPDATE User SET username = ? WHERE id = ?", (new_username, user_id))
        conn.commit()
        conn.close()
        return True

def update_password(user_id, new_password):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    hashed_password = hashlib.sha256((new_password).encode()).hexdigest()

    cursor.execute("UPDATE User SET password = ? WHERE id = ?", (hashed_password, user_id))
    conn.commit()
    conn.close()


def insert_admin_details(username, password, email,location,price):
    hashed_password = hash_password(password)  # Hash the admin password
    insert_query = """
    INSERT INTO admin (username, password, email,location,price) VALUES (?, ?, ?,?,?);
    """
    try:
        connection = sqlite3.connect('my_database.db')
        cursor = connection.cursor()
        cursor.execute(insert_query, (username, hashed_password, email,location,price))
        connection.commit()
        print('Admin details inserted successfully')
    except Error as e:
        print(e)

def get_admin_details(username):        
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin WHERE username = ?", (username,))
    user = cursor.fetchall()
    conn.close()
    return user

def get_admin_details_by_id(id):        
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admin WHERE id = ?", (id,))
    admin = cursor.fetchall()
    conn.close()
    return admin
   



def update_admin_username(admin_id, new_username):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    # Check if another user already has the same username
    cursor.execute("SELECT id FROM admin WHERE username = ? AND id != ?", (new_username, admin_id))
    existing_user_id = cursor.fetchone()

    if existing_user_id:
        # Another user already has this username, return False to indicate the update is not possible
        conn.close()
        return False
    else:
        # Update the username
        cursor.execute("UPDATE admin SET username = ? WHERE id = ?", (new_username, admin_id))
        conn.commit()
        conn.close()
        return True

def update_admin_location_price(admin_id, price):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE admin SET price = ? WHERE id = ?", (price, admin_id))
    conn.commit()
    conn.close()
    return True
      
     
def get_license_no(username):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT car_no FROM User WHERE username = ?", (username,))
    car_no = cursor.fetchone()
    conn.close()
    return car_no[0] if car_no else None

def new_user(username, email, password, car_no, mobile_no):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    hashed_password = hash_password(password)
    cursor.execute("INSERT INTO User (username, email, password, car_no, mobile_no) VALUES (?, ?, ?, ?, ?)",
                   (username, email, hashed_password, car_no, mobile_no))
    print("new user added")
    conn.commit()
    conn.close()
    
def check_password_hash(plain_password, hashed_password):
    return hashlib.sha256(plain_password.encode()).hexdigest() == hashed_password


def get_user_details_by_id(user_id):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user


def new_schedule(user_id, car_no, date_added, start_time, end_time, hours, location,parking_slot):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Schedule (id, car_no, date_added, start_time, end_time, hours, location, parking_slot) VALUES (?, ?, ?, ?, ?, ?, ?,?)",
                   (user_id, car_no, date_added, start_time, end_time, hours, location,parking_slot))
    conn.commit()
    conn.close()

def update_schedule(schedule_id, selected_schedule, amount_given):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE Schedule SET selected_schedule = ?, amount_given = ? WHERE id = ?",
                   (selected_schedule, amount_given, schedule_id))
    conn.commit()
    conn.close()

def delete_schedule(schedule_id):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Schedule WHERE id = ?", (schedule_id,))
    conn.commit()
    conn.close()

def get_user_schedules(user_id):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Schedule WHERE user_id = ?", (user_id,))
    schedules = cursor.fetchall()
    conn.close()
    return schedules


def get_admins_shedules(location):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Schedule WHERE location = ?", (location.capitalize(),))
    schedules = cursor.fetchall()
    conn.close()
    return schedules


def get_total_given_amount(user_id):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount_given) FROM Schedule WHERE user_id = ?", (user_id,))
    total_given_amount = cursor.fetchone()[0]
    conn.close()
    return total_given_amount




def check_schedule_reserve(date, start_time, end_time):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Schedule")
    schedules = cursor.fetchall()

    if len(schedules) != 0:
        for schedule in schedules:
            stored_date = schedule[3]
            stored_start_time = schedule[4]
            stored_end_time = schedule[5]

            if stored_date == date:
                if (start_time < stored_end_time) and (end_time > stored_start_time):
                    conn.close()
                    return [schedule[8],schedule[4],schedule[5]]  # Overlapping time, cannot reserve
    conn.close()
    return True  


        
def check_reservation(date,start_time,end_time,location):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM Schedule
        WHERE date_added = ? AND location = ? AND (
            (start_time <= ? AND ? <= end_time) OR
            (start_time <= ? AND ? <= end_time)
        )
    ''', (date,location, start_time, start_time, end_time, end_time))
    conflicts = cursor.fetchall()
    if conflicts:
        reservation =  []
        for conflict in conflicts: 
            reservation.append(int(conflict[7]))
        conn.close()
        return reservation
    else:
        conn.close()
        return []
        
    

def add_parking(user_id, date, start_time, end_time, parking_slot, location, price,car_license_no):
    try:
        # Connect to the SQLite database
        conn = sqlite3.connect('my_database.db')  
        cursor = conn.cursor()
        parking_id = generate_booking_id()
        cursor.execute("""
            INSERT INTO parkings (user_id, date, start_time, end_time, parking_slot, location, price,car_license_no,parking_id)
            VALUES (?, ?, ?, ?, ?, ?, ?,?,?)
        """, (user_id, date, start_time, end_time, parking_slot, location, price,car_license_no,parking_id))

        conn.commit()
        conn.close()

        print("Booking added successfully.")
    
    except Exception as e:
        print(f"Error adding booking: {str(e)}")
        
def get_user_parkings(user_id):
    try:
        conn = sqlite3.connect('my_database.db')  
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM parkings WHERE user_id = ?
        """, (user_id,))

        bookings = cursor.fetchall()

        conn.close()

        return bookings
    
    except Exception as e:
        print(f"Error getting user bookings: {str(e)}")
        return None


def generate_booking_id():
    return random.randint(1000, 9999)

if __name__ == '__main__':
    # create_database()
    insert_admin_details( 'admin1', 'admin_password', 'admin1@example.com',"SILVASSA",70)
    insert_admin_details( 'rishi', 'admin', 'admin1@example.com',"VAPI",80)