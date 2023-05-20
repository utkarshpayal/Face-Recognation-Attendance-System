#Face Recognition Attendance System

This is a Python script that implements a Face Recognition Attendance System using OpenCV, tkinter, face_recognition library, and MongoDB.
Installation

To run this script, you need to have the following dependencies installed:

    OpenCV (cv2)
    tkinter
    PIL (Image, ImageTk)
    face_recognition
    pickle
    pymongo
    datetime
    json

You can install these dependencies using pip:

pip install opencv-python
pip install tkinter
pip install pillow
pip install face-recognition
pip install pymongo

Usage

    Ensure that you have MongoDB installed and running on your system.

    Update the MongoDB connection details in the script by modifying the following variables:
        mongo_host: MongoDB host URL (default: "mongodb://localhost:27017")
        mongo_port: MongoDB port number (default: 27017)
        mongo_db: MongoDB database name (default: "face_recognition")
        mongo_collection: MongoDB collection name for storing captured images (default: "captured_images")

    Run the script using the following command:

    python script_name.py

    The script will open a GUI window displaying the video feed from the default camera. It will recognize faces in real-time and mark attendance if a recognized face is detected.

    To capture an image for attendance, click the "Capture Image" button. A password window will appear where you need to enter the password (default: "password"). After entering the correct password, the script will capture an image and prompt you to enter the name for the captured image in a new window.

    The captured image will be saved to disk as "captured_image.jpg" and also stored in the MongoDB collection specified in the connection details.

    The attendance count for each recognized face will be displayed in the GUI window.

    To close the camera and exit the script, click the "Close" button or close the GUI window.

Additional Notes

    The script uses a known_faces.pkl file to store the encodings and names of known faces. If the file does not exist, it will be created automatically when known faces are added.

    The script saves the attendance data to "attendance.json" and last attendance data to "last_attendance.json" files. These files store the attendance count and last attendance time for each recognized face. If the files do not exist, they will be created automatically.

    The attendance data is loaded at the start of the script, and the last attendance data is checked to prevent duplicate attendance within 24 hours.

    You can adjust the tolerance value in the recognize_faces() function to control the face recognition accuracy. Lower tolerance values make face recognition stricter, while higher values make it more lenient.

    The script uses tkinter for creating a simple GUI to display the video feed and attendance information.

    Make sure to have a webcam or camera connected to your system for capturing the video feed.

Feel free to customize the script as per your requirements and extend its functionality.
