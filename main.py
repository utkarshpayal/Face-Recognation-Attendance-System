import cv2
import tkinter as tk
from PIL import Image, ImageTk
import face_recognition
import pickle
from datetime import datetime, timedelta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import threading
import queue
import os
import pandas as pd

# File to store known face encodings and names
known_faces_file = "known_faces.pkl"

# Global variables for face recognition and attendance
known_face_encodings = []
known_face_names = []
attendance = {}
last_attendance = {}
sender_email = "t8196382@gmail.com"
sender_password = "hexltljbdqfuwlov"
receiver_email = "utkarsh12march2004@gmail.com"

# Function to load known face encodings and names from a file
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

# Function to save known face encodings and names to a file
def save_known_faces():
    data = {"encodings": known_face_encodings, "names": known_face_names}
    with open(known_faces_file, "wb") as file:
        pickle.dump(data, file)

# Function to check if a person can mark attendance (to prevent duplicate entries)
def can_mark_attendance(name):
    if name not in last_attendance:
        return True
    else:
        last_marked_time = last_attendance[name]
        current_time = datetime.now()
        time_difference = current_time - last_marked_time
        return time_difference >= timedelta(seconds=10)

# Function to send an email
def send_email(subject, body):
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, receiver_email, message.as_string())
            print("Email sent successfully!")
    except smtplib.SMTPException as e:
        print("Failed to send email:", str(e))

# Function to update the status label in the GUI
def update_status(message, color="black"):
    status_label.config(text=message, fg=color)

# Function to update the attendance display in the GUI
def update_attendance_display():
    attendance_text = "\n".join([f"{name}: {count}" for name, count in attendance.items()])
    attendance_display.config(text=attendance_text)

# Function to display the attendance in a new window
def display_attendance():
    attendance_window = tk.Toplevel(root)
    attendance_window.title("Attendance")

    if len(attendance) == 0:
        empty_label = tk.Label(attendance_window, text="No attendance marked.")
        empty_label.pack()
    else:
        for name, count in attendance.items():
            attendance_label = tk.Label(attendance_window, text=f"{name}: {count}")
            attendance_label.pack()

# Function to capture an image from the camera
def capture_image():
    _, frame = cap.read()
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame)
    image.save("captured_image.jpg")
    update_status("Image captured successfully!", "green")

    name_window = tk.Toplevel(root)
    name_window.title("Enter Name")
    name_label = tk.Label(name_window, text="Enter name:")
    name_label.pack()
    name_entry = tk.Entry(name_window)
    name_entry.pack()
    save_button = tk.Button(
        name_window, text="Save", command=lambda: save_name(name_window, name_entry.get())
    )
    save_button.pack()

# Function to save the name and face encoding of a person
def save_name(name_window, name):
    global known_face_encodings, known_face_names

    directory_path = os.path.join("captured_images", name)
    os.makedirs(directory_path, exist_ok=True)

    image = face_recognition.load_image_file("captured_image.jpg")
    encoding = face_recognition.face_encodings(image)

    if len(encoding) > 0:
        known_face_encodings.append(encoding[0])
        known_face_names.append(name)

        save_known_faces()

        image_path = os.path.join(directory_path, f"{name}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg")
        image_pil = Image.fromarray(image)
        image_pil.save(image_path)

        print("Name and image saved successfully!")
    else:
        print("No face detected in the captured image.")

    name_window.destroy()

# Function to close the camera and exit the program
def close_camera():
    cap.release()
    cv2.destroyAllWindows()
    root.destroy()

# Function to recognize faces in the camera feed
def recognize_faces(frame):
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    small_frame = cv2.resize(rgb_frame, (0, 0), fx=0.25, fy=0.25)  # Reduce frame size for faster processing
    face_locations = face_recognition.face_locations(small_frame)
    face_encodings = face_recognition.face_encodings(small_frame, face_locations)

    face_names = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        name = "Unknown"

        if True in matches:
            matched_index = matches.index(True)
            name = known_face_names[matched_index]

            if can_mark_attendance(name):
                attendance[name] = attendance.get(name, 0) + 1
                last_attendance[name] = datetime.now()
                send_email("Match Found", f"{name} is seen in the camera. ")

        face_names.append(name)

    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, name, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    return frame

# Function to save attendance data to an Excel file
def save_attendance_to_excel():
    if len(attendance) == 0:
        update_status("No attendance data to save.", "red")
        return

    today = datetime.now().strftime("%d%b")
    attendance_file = "attendance.xlsx"

    if os.path.exists(attendance_file):
        df = pd.read_excel(attendance_file, index_col=0)
    else:
        df = pd.DataFrame()

    # Create the necessary columns if the DataFrame is empty
    if len(df.columns) == 0:
        df[today] = 0

    for name, count in attendance.items():
        if name not in df.index:
            df.loc[name] = [0] * len(df.columns)

        df.at[name, today] = count

    df.to_excel(attendance_file)
    update_status(f"Attendance data saved to {attendance_file}", "green")

# Initialize the camera and create the GUI
cap = cv2.VideoCapture(0)

root = tk.Tk()
root.title("Face Recognition")
root.geometry("800x700")

frame_top = tk.Frame(root, bg="lightgray")
frame_top.pack(fill=tk.BOTH, expand=True)

frame_middle = tk.Frame(root)
frame_middle.pack()

frame_bottom = tk.Frame(root)
frame_bottom.pack()
canvas = tk.Canvas(frame_top, width=800, height=500, bg="black")
canvas.pack()

status_label = tk.Label(frame_middle, text="", fg="black")
status_label.pack()

attendance_label = tk.Label(frame_middle, text="Attendance", font=("Helvetica", 16, "bold"))
attendance_label.pack()

attendance_display = tk.Label(frame_middle, text="", fg="blue", font=("Helvetica", 12))
attendance_display.pack()

capture_button = tk.Button(
    frame_bottom,
    text="Capture Image",
    command=capture_image,
    bg="green",
    fg="white",
    font=("Helvetica", 14, "bold"),
    relief=tk.GROOVE,
    padx=20,
    pady=10,
)
capture_button.pack(side=tk.LEFT, padx=10)

attendance_button = tk.Button(
    frame_bottom,
    text="Show Attendance",
    command=display_attendance,
    bg="blue",
    fg="white",
    font=("Helvetica", 14, "bold"),
    relief=tk.GROOVE,
    padx=20,
    pady=10,
)
attendance_button.pack(side=tk.LEFT, padx=10)

# Add the button to save attendance to Excel
save_excel_button = tk.Button(
    frame_bottom,
    text="Save Attendance to Excel",
    command=save_attendance_to_excel,
    bg="orange",
    fg="white",
    font=("Helvetica", 14, "bold"),
    relief=tk.GROOVE,
    padx=20,
    pady=10,
)
save_excel_button.pack(side=tk.LEFT, padx=10)

close_button = tk.Button(
    frame_bottom,
    text="Exit",
    command=close_camera,
    bg="red",
    fg="white",
    font=("Helvetica", 14, "bold"),
    relief=tk.GROOVE,
    padx=20,
    pady=10,
)
close_button.pack(side=tk.LEFT, padx=10)

frame_queue = queue.Queue(maxsize=5)

def video_capture_thread():
    while True:
        ret, frame = cap.read()
        if ret:
            frame_queue.put(frame)
        else:
            update_status("Error: Unable to retrieve frame from camera.", "red")
            break

def process_frame():
    try:
        frame = frame_queue.get_nowait()
        update_canvas(frame)
    except queue.Empty:
        pass

    root.after(10, process_frame)

def update_canvas(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = recognize_faces(frame)

    image = Image.fromarray(frame)
    image_tk = ImageTk.PhotoImage(image)

    canvas.create_image(0, 0, anchor=tk.NW, image=image_tk)
    canvas.image = image_tk

    update_attendance_display()

if __name__ == "__main__":
    video_thread = threading.Thread(target=video_capture_thread, daemon=True)
    video_thread.start()

    load_known_faces()
    process_frame()

    root.mainloop()

    cap.release()
    cv2.destroyAllWindows()
