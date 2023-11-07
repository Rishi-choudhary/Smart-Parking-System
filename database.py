import sqlite3
import hashlib

def create_database():
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
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
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            car_no TEXT,
            date_added DATE,
            start_time TIME,
            end_time TIME,
            hours REAL,
            FOREIGN KEY (user_id) REFERENCES User(id),
            parking_slot INTEGER
        )
    ''')
    conn.commit()
    conn.close()

def hash_password(password):
    # Hash the password before storing it in the database
    return hashlib.sha256(password.encode()).hexdigest()

def get_user_details(username):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM User WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    print(user)
    return user

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



def new_schedule(user_id, car_no, date_added, start_time, end_time, hours):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Schedule (user_id, car_no, date_added, start_time, end_time, hours) VALUES (?, ?, ?, ?, ?, ?)",
                   (user_id, car_no, date_added, start_time, end_time, hours))
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

def get_total_given_amount(user_id):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount_given) FROM Schedule WHERE user_id = ?", (user_id,))
    total_given_amount = cursor.fetchone()[0]
    conn.close()
    return total_given_amount



