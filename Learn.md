Face Recognition Attendance System

This project is a Face Recognition Attendance System implemented in Python using machine learning techniques. The system uses the OpenCV library for face detection and recognition, and it integrates with a MongoDB database to store captured images and attendance data.
Dependencies

Before running the project, make sure you have the following dependencies installed:

    Python (version 3.x)
    OpenCV (Open Source Computer Vision Library)
    tkinter (Python GUI toolkit)
    PIL (Python Imaging Library)
    face-recognition (Python library for face recognition)
    pymongo (Python driver for MongoDB)

You can install the required Python libraries using pip:

shell

pip install opencv-python tkinter pillow face-recognition pymongo

Usage

    Clone the project repository:

    shell

git clone <repository-url>

Navigate to the project directory:

shell

cd face-recognition-attendance-system

Start a local instance of MongoDB server on localhost:27017.

Run the main.py file to launch the Face Recognition Attendance System:

shell

    python main.py

    This will open a GUI window displaying the video feed from your webcam and the attendance count for recognized individuals.

    Capture an image for attendance:
        Click on the "Capture Image" button to capture an image from the webcam.
        Enter the password "password" in the password window to proceed with capturing an image.

    The captured image will be saved, and a new window will appear to enter the name for the captured image.

    Enter the name for the captured image in the "Enter Name" window and click the "Save" button.
        The captured image will be processed for face recognition, and if a face is detected, the name will be associated with the recognized face.
        The name and face encoding will be added to the known faces database for future recognition.

    The attendance count for recognized individuals will be displayed in the GUI window.
        The attendance count is updated every time a recognized face is detected.
        The attendance data is stored in a MongoDB database.

    To exit the application, click the "Close" button or close the GUI window.
        The attendance data, known faces, and last attendance information will be saved in files (attendance.json, last_attendance.json, and known_faces.pkl respectively) for future use.

Note: Make sure to have a well-aligned and clear face for better recognition accuracy. Also, remember to periodically update the known faces database and retrain the model to improve recognition performance.

Feel free to modify the instructions and information according to your specific project requirements. This is just a basic example to give you an idea of how the learn.md file for your Face Recognition Attendance System project could be structured.

If you have any further questions or need assistance with any specific aspect of the project, please let me know.
