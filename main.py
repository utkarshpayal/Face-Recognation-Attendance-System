import cv2
import tkinter as tk
from PIL import Image, ImageTk
import face_recognition
import pickle
from pymongo import MongoClient
from datetime import datetime, timedelta
import json

known_faces_file = "known_faces.pkl"
known_face_encodings = []
known_face_names = []
attendance = {}  # Attendance dictionary
last_attendance = {}  # Last attendance dictionary to track the last marked attendance

# MongoDB connection details
mongo_host = "mongodb://localhost:27017"
mongo_port = 27017
mongo_db = "face_recognition"
mongo_collection = "captured_images"

# Connect to MongoDB
client = MongoClient(mongo_host, mongo_port)
db = client[mongo_db]
collection = db[mongo_collection]

def close_camera():
    display_attendance([])
    save_known_faces()
    cap.release()
    cv2.destroyAllWindows()
    root.destroy()

def capture_image():
    password_window = tk.Toplevel(root)
    password_window.title("Enter Password")
    password_label = tk.Label(password_window, text="Enter password:")
    password_label.pack()
    password_entry = tk.Entry(password_window, show="*")
    password_entry.pack()
    verify_button = tk.Button(password_window, text="Verify", command=lambda: verify_password(password_window, password_entry.get()))
    verify_button.pack()

def verify_password(password_window, entered_password):
    if entered_password == "password":
        password_window.destroy()
        _, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(frame)
        image.save("captured_image.jpg")
        print("Image captured successfully!")

        # Open a new window to enter the name for the captured image
        capture_window = tk.Toplevel(root)
        capture_window.title("Enter Name")
        name_label = tk.Label(capture_window, text="Enter name:")
        name_label.pack()
        name_entry = tk.Entry(capture_window)
        name_entry.pack()
        save_button = tk.Button(capture_window, text="Save", command=lambda: save_name(capture_window, name_entry.get()))
        save_button.pack()
    else:
        print("Incorrect password")

def save_name(capture_window, name):
    global known_face_encodings, known_face_names

    # Load the captured image and encode the face
    image = face_recognition.load_image_file("captured_image.jpg")
    encoding = face_recognition.face_encodings(image)

    # If a face is detected, add the name and encoding to the known faces
    if len(encoding) > 0:
        known_face_encodings.append(encoding[0])
        known_face_names.append(name)

        save_known_faces()
        save_image_to_db("captured_image.jpg", name)  # Save image to MongoDB

        print("Name saved successfully!")
    else:
        print("No face detected in the captured image.")

    # Close the capture window
    capture_window.destroy()

def save_known_faces():
    data = {"encodings": known_face_encodings, "names": known_face_names}
    with open(known_faces_file, "wb") as file:
        pickle.dump(data, file)

    # Save attendance data to a JSON file
    with open("attendance.json", "w") as file:
        json.dump(attendance, file)

    # Save last attendance data to a JSON file
    with open("last_attendance.json", "w") as file:
        # Convert last_attendance values from datetime objects to string
        last_attendance_str = {name: time.isoformat() for name, time in last_attendance.items()}
        json.dump(last_attendance_str, file)

def load_known_faces():
    global known_face_encodings, known_face_names
    try:
        with open(known_faces_file, "rb") as file:
            data = pickle.load(file)
            known_face_encodings = data["encodings"]
            known_face_names = data["names"]
            print("Known faces loaded successfully!")
    except FileNotFoundError:
        print("No known faces found. Train the faces first.")

    # Load attendance data from file, if available
    try:
        with open("attendance.json", "r") as file:
            attendance_data = json.load(file)
            attendance.update(attendance_data)
            print("Attendance data loaded successfully!")
    except FileNotFoundError:
        print("No attendance data found.")

    # Load last attendance data from file, if available
    try:
        with open("last_attendance.json", "r") as file:
            last_attendance_data = json.load(file)
            # Convert last_attendance values from string to datetime objects
            last_attendance.update({name: datetime.fromisoformat(time) for name, time in last_attendance_data.items()})
            print("Last attendance data loaded successfully!")
    except FileNotFoundError:
        print("No last attendance data found.")

def recognize_faces(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        tolerance = 0.5  # Adjust the tolerance value as per your requirement
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=tolerance)
        name = "Unknown"

        if True in matches:
            matched_index = matches.index(True)
            name = known_face_names[matched_index]

            # Check if attendance can be marked
            if can_mark_attendance(name):
                attendance[name] = attendance.get(name, 0) + 1  # Update attendance count
                last_attendance[name] = datetime.now()  # Update last attendance time
                print("Attendance marked for", name)
            else:
                print("Attendance already marked for", name, "within the last 24 hours.")

        face_names.append(name)

    display_attendance(face_names)

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return frame

def show_frame():
    _, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = recognize_faces(frame)
    image = Image.fromarray(frame)
    image_tk = ImageTk.PhotoImage(image)
    panel.configure(image=image_tk)
    panel.image = image_tk
    root.after(10, show_frame)

def save_image_to_db(image_path, name):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        image_doc = {"name": name, "image_data": image_data}
        collection.insert_one(image_doc)
        print("Image saved to MongoDB")

def can_mark_attendance(name):
    if name not in last_attendance:
        return True
    else:
        last_marked_time = last_attendance[name]
        current_time = datetime.now()
        time_difference = current_time - last_marked_time
        return time_difference > timedelta(days=1)

def display_attendance(face_names):
    attendance_text = ""
    for name in face_names:
        attendance_text += name + ": " + str(attendance.get(name, 0)) + "\n"

    attendance_label.configure(text=attendance_text)

# Load known faces and attendance data
load_known_faces()

# Initialize the video capture
cap = cv2.VideoCapture(0)

# Create a GUI window using tkinter
root = tk.Tk()
root.title("Face Recognition Attendance System")

# Create a label to display the video feed
panel = tk.Label(root)
panel.pack(side="top", padx=10, pady=10)

# Create a label to display attendance
attendance_label = tk.Label(root)
attendance_label.pack(side="bottom", padx=10, pady=10)

# Create a button to capture an image
capture_button = tk.Button(root, text="Capture Image", command=capture_image)
capture_button.pack(side="bottom", padx=10, pady=10)

# Create a button to close the camera
close_button = tk.Button(root, text="Close", command=close_camera)
close_button.pack(side="bottom", padx=10, pady=10)

# Start the video capture and display the video feed
show_frame()

# Run the GUI event loop
root.mainloop()
