# Face Recognition Attendance System

A Python desktop application that recognises faces from a webcam feed, marks attendance for known people, sends an email notification when a known person is seen, and can export the attendance counts to an Excel file. The GUI is built with Tkinter and face recognition is done with the `face_recognition` library.

## Features

- Live webcam feed in a Tkinter window, with a green box and name drawn around each detected face (`Unknown` for unrecognised faces).
- **Capture Image**: captures the current frame, asks for a name, computes the face encoding and adds it to the known-faces store.
- Automatic attendance: each time a known face is recognised its attendance count is incremented, with a 10-second cooldown per person to avoid duplicate entries.
- Email notification ("Match Found") via Gmail SMTP whenever attendance is marked.
- **Show Attendance**: opens a window listing each name and its count.
- **Save Attendance to Excel**: writes the counts into `attendance.xlsx`, in a column named after the current date (e.g. `11Nov`).
- **Exit**: releases the camera and closes the app.

## Tech stack

- Python 3
- [OpenCV](https://pypi.org/project/opencv-python/) (`cv2`) for camera capture and drawing
- [face_recognition](https://pypi.org/project/face-recognition/) (requires `dlib`) for face detection and encodings
- Tkinter and [Pillow](https://pypi.org/project/pillow/) for the GUI
- [pandas](https://pypi.org/project/pandas/) for the Excel export
- Standard library: `pickle`, `smtplib`, `email`, `threading`, `queue`, `datetime`, `os`

## Installation

```sh
git clone https://github.com/utkarshpayal/Face-Recognation-Attendance-System.git
cd Face-Recognation-Attendance-System
pip install opencv-python pillow face-recognition pandas openpyxl
```

Notes:

- Tkinter ships with most Python installers; on some Linux distributions it is a separate package (e.g. `python3-tk`).
- `face-recognition` depends on `dlib`, which needs CMake and a C++ compiler to build.
- `openpyxl` is needed by pandas to read/write `.xlsx` files.

## Configuration

Email settings are hard-coded as variables near the top of `main.py`; there are no environment variables or config files. Set them before running:

| Variable | Purpose |
| --- | --- |
| `sender_email` | Gmail address used to send notifications |
| `sender_password` | Password / app password for that Gmail account |
| `receiver_email` | Address that receives the "Match Found" emails |

Gmail SMTP (`smtp.gmail.com:587`, STARTTLS) is used. Do not commit real credentials to the repository; consider loading them from environment variables instead.

The camera used is device `0` (`cv2.VideoCapture(0)`).

## Usage

```sh
python main.py
```

1. Click **Capture Image** while a person is in front of the camera, type their name and click **Save**.
2. When that person appears in the feed again, their attendance is counted and an email is sent.
3. Use **Show Attendance** to view counts or **Save Attendance to Excel** to export them.
4. Click **Exit** to close the camera and the app.

## Files created at runtime

| Path | Contents |
| --- | --- |
| `known_faces.pkl` | Pickled face encodings and names (loaded on start-up if present) |
| `captured_image.jpg` | The most recent captured frame |
| `captured_images/<name>/` | Saved images for each registered person |
| `attendance.xlsx` | Exported attendance table |

Attendance counts are kept in memory and are only persisted when you click **Save Attendance to Excel**.

## Other docs

`Learn.md` describes an earlier version of the project (MongoDB storage and a password prompt before capturing). Neither is used by the current `main.py`.

## License

This project is licensed under the [Apache License 2.0](LICENSE).
