from flask import redirect, render_template, session
import json
from functools import wraps
from datetime import datetime


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

# def update_parking_data():
#     # Implement your data processing logic here
#     while True:
#         new_data = parking_space()  # Implement your data retrieval logic
#         if new_data != previous_data:
#             previous_data = new_data
#             return new_data