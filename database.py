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
            user_id INTEGER,
            car_no TEXT,
            date_added DATE,
            start_time TIME,
            end_time TIME,
            hours INT,
            location TEXT,
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

def update_username(user_id, new_username):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()

    # Check if another user already has the same username
    cursor.execute("SELECT id FROM User WHERE username = ? AND id != ?", (new_username, user_id))
    existing_user_id = cursor.fetchone()

    if existing_user_id:
        # Another user already has this username, return False to indicate the update is not possible
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

    # Hash and salt the new password (replace 'salt' with an actual salt value)
    hashed_password = hashlib.sha256((new_password).encode()).hexdigest()

    cursor.execute("UPDATE User SET password = ? WHERE id = ?", (hashed_password, user_id))
    conn.commit()
    conn.close()






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


def new_schedule(user_id, car_no, date_added, start_time, end_time, hours, location,parking_slot):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Schedule (user_id, car_no, date_added, start_time, end_time, hours, location, parking_slot) VALUES (?, ?, ?, ?, ?, ?, ?,?)",
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

def get_total_given_amount(user_id):
    conn = sqlite3.connect('my_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT SUM(amount_given) FROM Schedule WHERE user_id = ?", (user_id,))
    total_given_amount = cursor.fetchone()[0]
    conn.close()
    return total_given_amount



import sqlite3

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

            # Check for overlapping time slots
            if stored_date == date:
                if (start_time < stored_end_time) and (end_time > stored_start_time):
                    conn.close()
                    return [schedule[8],schedule[4],schedule[5]]  # Overlapping time, cannot reserve
    conn.close()
    return True  # No overlap, safe to reserve
