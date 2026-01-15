# Face Recognition Attendance System (Python)

This project is a Python-based face recognition attendance system that automatically detects faces using a webcam and records attendance in real time.

The system identifies known faces, logs attendance with timestamps, generates reports, and sends the attendance details automatically through email and WhatsApp.

This project was built to understand how computer vision, automation, and Python libraries can work together in a real-world application.

---

## Project Features

The system performs the following tasks:

* Detects faces in real time using a webcam
* Recognizes known faces from training images
* Records attendance with name and time
* Stores attendance in CSV and TXT formats
* Generates an Excel attendance report automatically
* Sends the attendance report to email
* Sends a WhatsApp notification after report generation

---

## How It Works

1. Training images are loaded from the `Training_images` folder
2. Faces are encoded using the `face_recognition` library
3. The webcam captures live video
4. Detected faces are matched with known encodings
5. Attendance is recorded with timestamps
6. An Excel report is generated at the end of the session
7. The report is sent via email
8. A WhatsApp message is sent confirming report delivery

Press **Q** or **ESC** to stop the system.

---

## Files Overview

attendance_full.py
Main file that runs the complete face attendance system

Training_images/
Folder containing images of known people used for face recognition

Attendance.csv
Stores attendance records in CSV format

Attendance.txt
Stores attendance logs in text format

Attendance_<date>_<time>.xlsx
Automatically generated Excel attendance report

mail.py / excel2.py (if present)
Supporting scripts used during development

---

## Technologies and Libraries Used

* Python
* OpenCV (cv2)
* face_recognition
* NumPy
* OpenPyXL
* yagmail (for email automation)
* pywhatkit (for WhatsApp automation)

---

## Requirements

Before running the project, install the required libraries:

```
pip install opencv-python face-recognition numpy openpyxl yagmail pywhatkit
```

A webcam is required for face detection.

---

## Use Case

This project can be used for:

* Classroom attendance systems
* Office or lab attendance tracking
* Learning computer vision and automation
* Python mini or academic projects

---

## Notes

* Training images must contain clear front-facing photos
* Each image file name should match the person’s name
* Email and WhatsApp credentials must be configured before running

This project focuses on learning and practical implementation rather than production deployment.

---

## Author

Aravind Ganipisetty



