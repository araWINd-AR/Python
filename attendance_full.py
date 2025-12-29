import cv2
import numpy as np
import face_recognition
import os
import csv
import datetime
import openpyxl
import yagmail
import pywhatkit


# CONFIG

TRAIN_DIR = "Training_images"
CSV_FILE = "Attendance.csv"
TXT_FILE = "Attendance.txt"

# Email config 
SENDER_EMAIL = "aravindganipisetty@gmail.com"
APP_PASSWORD = "ttziriyqpmolgidq"     
RECEIVER_EMAIL = "ganipisettyaravind@gmail.com"

# WhatsApp config 
WHATSAPP_NUMBER = "+917993795905"     


 
#  Load + Encode Training Images

def load_training_images():
    encodings = []
    names = []

    print("\n Loading Training Images...")

    for file in os.listdir(TRAIN_DIR):
        if file.lower().endswith((".jpg", ".jpeg", ".png")):
            full_path = os.path.join(TRAIN_DIR, file)
            img = cv2.imread(full_path)

            if img is None:
                print(f" Could not read {file}")
                continue

            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            encode = face_recognition.face_encodings(rgb)

            if len(encode) == 0:
                print(f" No face in {file}")
                continue

            encodings.append(encode[0])
            names.append(os.path.splitext(file)[0])
            print(f" Encoded: {file}")

    if not encodings:
        raise SystemExit(" No valid training images found!")

    print("Classes detected:", names)
    return encodings, names


#  Attendance Logging

def log_csv(name, time):
    create_header = not os.path.exists(CSV_FILE)

    with open(CSV_FILE, "a", newline="") as f:
        writer = csv.writer(f)
        if create_header:
            writer.writerow(["Name", "Time"])
        writer.writerow([name, time])


def log_txt(name, time):
    with open(TXT_FILE, "a") as f:
        f.write(f"{name} | {time}\n")


def mark_attendance(name, session_log):
    now = datetime.datetime.now().strftime("%H:%M:%S")
    session_log.append((name, now))
    log_csv(name, now)
    log_txt(name, now)
    print(f" Attendance Recorded: {name} at {now}")



# Export to Excel

def export_excel(session_log):
    if not session_log:
        print(" No attendance to export.")
        return None

    timestamp = datetime.datetime.now().strftime("%d-%b-%Y__%H_%M_%S")
    filename = f"Attendance_{timestamp}.xlsx"

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Attendance"

    ws.append(["Name", "Time"])
    for name, time in session_log:
        ws.append([name, time])

    wb.save(filename)
    print(f" Excel created: {filename}")
    return filename



# Send Email

def send_email(excel_file, session_log):
    if excel_file is None:
        print(" No Excel file to send.")
        return

    subject = f"Attendance Report - {datetime.datetime.now().strftime('%d-%b-%Y %H:%M:%S')}"

    unique_names = sorted({name for name, _ in session_log})
    body = f"""

    Hello,

    Please find the attendance report attached.

    Total Records: {len(session_log)}
    People Present: {", ".join(unique_names)}

    Regards,
    Face Attendance System
    """

    attachments = [excel_file]
    if os.path.exists(CSV_FILE): attachments.append(CSV_FILE)
    if os.path.exists(TXT_FILE): attachments.append(TXT_FILE)

    print(f" Sending Email: {attachments}")

    try:
        yag = yagmail.SMTP(SENDER_EMAIL, APP_PASSWORD)
        yag.send(
            to=RECEIVER_EMAIL,
            subject=subject,
            contents=body,
            attachments=attachments,
        )
        print(" Email sent!")
    except Exception as e:
        print(" Email error:", e)


#  Send WhatsApp Message

def send_whatsapp(excel_file):
    if excel_file is None:
        return

    msg = f"The attendence report shared to your email , the file name is : Attendance report generated.\nFile: {excel_file}"

    try:
        print(" Sending WhatsApp message...")
        pywhatkit.sendwhatmsg_instantly(WHATSAPP_NUMBER, msg)
        print(" WhatsApp message sent automatically!")
    except Exception as e:
        print(" WhatsApp Error:", e)



#  MAIN SYSTEM

def main():
    known_encodings, names = load_training_images()
    session_log = []

    cap = cv2.VideoCapture(0)
    print("\n Webcam running... Press Q or ESC to exit.")

    while True:
        ok, frame = cap.read()
        if not ok:
            print(" Camera error")
            break

        small = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
        rgb = cv2.cvtColor(small, cv2.COLOR_BGR2RGB)

        faces = face_recognition.face_locations(rgb)
        encodes = face_recognition.face_encodings(rgb, faces)

        for encode, faceLoc in zip(encodes, faces):
            matches = face_recognition.compare_faces(known_encodings, encode)
            dist = face_recognition.face_distance(known_encodings, encode)

            best = np.argmin(dist)

            if matches[best]:
                name = names[best].upper()
                mark_attendance(name, session_log)

                y1, x2, y2, x1 = [v * 4 for v in faceLoc]
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.putText(frame, name, (x1, y1 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.imshow("Attendance System", frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord("q") or key == 27:
            print("\n Closing system...")
            break

    cap.release()
    cv2.destroyAllWindows()

    excel_file = export_excel(session_log)
    send_email(excel_file, session_log)
    send_whatsapp(excel_file)


if __name__ == "__main__":
    main()
