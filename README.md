# Smart Parking System

![Demo Image](demo.png)

The Smart Parking System is a web-based application designed to monitor and manage parking spaces in real-time using computer vision technology and Flask as the web server. This project is intended to help you create a smart parking management system with features like real-time status updates, reservation capabilities, and more.

## Features

- Real-time parking slot occupancy detection using OpenCV
- Web-based interface for users to check parking availability and make reservations
- Automatic reservation expiration and release of slots upon no-show
- Easy-to-use and responsive design for both desktop and mobile devices
- Admin interface for monitoring and managing parking slots
- Customizable configuration options for different parking lots

## Requirements

- Python 3.x
- Flask (web server)
- OpenCV (computer vision for real-time slot detection)
- HTML, CSS, and JavaScript for the front-end
- Webcam or IP camera for real-time video feed
- Access to a web server (local or remote) to host the system

## Getting Started

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/smart-parking-system.git
Install the required Python packages:

bash
Copy code
pip install flask opencv-python
Modify the configuration in config.py to suit your parking lot's settings.

Start the Flask application:

bash
Copy code
python main.py
Access the web application in your browser at http://localhost:5000 (by default).

Integrate the camera system to capture real-time parking lot images and update the status.

# Usage
Users can visit the web application to check parking availability and make reservations.


Admins can access the admin panel by navigating to /admin to monitor and manage parking slots.

To integrate your camera system, ensure that it provides real-time images and update the /reserve route in main.py to capture and process the camera feed.



# some images of my project
![Screenshot 2023-11-04 223302](https://github.com/Rishi-choudhary/Smart-Parking-System/assets/77925291/e9efd826-66f6-400a-9946-413190b50857)

![Screenshot 2023-11-04 224413](https://github.com/Rishi-choudhary/Smart-Parking-System/assets/77925291/d416a2d3-0d1b-4c53-9b1a-7a1ce6f79aac)


![Screenshot 2023-11-04 223302](https://github.com/Rishi-choudhary/Smart-Parking-System/assets/77925291/658ee5ca-3e46-4f5a-8848-5391297a7b83)

![Screenshot 2023-11-04 223917](https://github.com/Rishi-choudhary/Smart-Parking-System/assets/77925291/58e2f146-5b65-4317-bf46-d5b8b68b3936)


# Contributing
Contributions to this project are welcome. You can contribute by opening issues, providing feedback, or submitting pull requests. Feel free to fork the project and make enhancements.

# License
This project is licensed under the MIT License - see the LICENSE file for details.

# Acknowledgments
This project was inspired by the need for efficient parking space management.
Special thanks to the Flask and OpenCV communities for their valuable contributions.
# Contact
If you have any questions or need assistance, please feel free to contact Rishi Choudhary - rishichoudhary582@gmail.com






