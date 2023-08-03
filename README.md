# Face Recognition and Attendance System

This is a Python application that performs face recognition using the `face_recognition` library and maintains attendance records. It captures images from a camera feed, recognizes faces, and marks attendance. The attendance data can be saved to an Excel file.

## Prerequisites

Before running the application, make sure you have the following libraries installed:

- OpenCV (`cv2`)
- Tkinter (`tk`)
- Pillow (`PIL`)
- `face_recognition`
- `pickle`
- `datetime`
- `smtplib`
- `email.mime.multipart`
- `email.mime.text`
- `threading`
- `queue`
- `os`
- `pandas`

You can install these dependencies using the following command:


```pip install opencv-python-headless pillow face-recognition pandas```


Usage


Clone this repository to your local machine.
Open a terminal and navigate to the project directory.
Run the following command to start the application:

```python main.py```

The application will open with a GUI. Follow the on-screen instructions to perform the following actions:
Capture an image of a person's face for recognition and attendance.
Display the current attendance records.
Save attendance data to an Excel file.
Exit the application.
Important Notes
The application uses Gmail to send email notifications. Make sure to replace the sender_email and sender_password variables with your own Gmail credentials. Also, set the receiver_email to the desired recipient's email address.

Known face encodings and names are stored in the known_faces.pkl file. If the file does not exist, it will be created when you save the first person's name and face.

To prevent duplicate attendance entries, a time delay of 10 seconds is applied for each person.

The captured images are stored in the captured_images directory.

Attendance data is saved to an Excel file named attendance.xlsx.

Make sure to grant camera access to the application when prompted.

License
This project is licensed under the MIT License.

