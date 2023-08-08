import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "https://schoolattendance-f10d2-default-rtdb.firebaseio.com/",
    'storageBucket': "schoolattendance-f10d2.appspot.com"
})



global captured_image
captured_image = None

def capture_image():
    global captured_image
    cap = cv2.VideoCapture(0)  # Change the camera index to the appropriate one if needed
    cap.set(3, 640)
    cap.set(4, 480)

    # Allow the camera to warm up for a few seconds
    for _ in range(30):
        cap.read()

    # Capture an image
    ret, frame = cap.read()
    if ret:
        captured_image = frame

    # Release the camera and close the window after a delay
    cap.release()
    cv2.destroyAllWindows()

def encode_student():
    folderPath = 'Images'
    pathList = os.listdir(folderPath)
    imgList = []
    studentIds = []

    for path in pathList:
        imgList.append(face_recognition.load_image_file(os.path.join(folderPath, path)))
        studentIds.append(os.path.splitext(path)[0])

    encodeListKnown = findEncodings(imgList)
    encodeListKnownWithIds = [encodeListKnown, studentIds]

    file = open("EncodeFile.p", 'wb')
    pickle.dump(encodeListKnownWithIds, file)
    file.close()

def findEncodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        face_encodings = face_recognition.face_encodings(img)
        if len(face_encodings) > 0:
            encodeList.append(face_encodings[0])
        else:
            print(f"No face detected in {img}")
    return encodeList

def register_student():
    global name_entry, major_entry, starting_year_entry, standing_entry, year_entry, last_attendance_time_entry
    global captured_image  # Use the global captured_image variable

    name = name_entry.get()
    major = major_entry.get()
    starting_year = starting_year_entry.get()
    standing = standing_entry.get()
    year = year_entry.get()
    last_attendance_time = last_attendance_time_entry.get()

    if not name or not major or not starting_year or not standing or not year or not last_attendance_time:
        messagebox.showerror("Error", "Please fill in all the fields.")
        return

    try:
        starting_year = int(starting_year)
        year = int(year)
    except ValueError:
        messagebox.showerror("Error", "Invalid input for starting year or year.")
        return
    if captured_image is not None:
        # Resize and encode the captured image
        imgS = cv2.resize(captured_image, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        encode_face = face_recognition.face_encodings(imgS)[0]

        # Save the captured image locally
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        image_filename = f"{name}_{timestamp}.png"
        cv2.imwrite(image_filename, captured_image)

        # Upload the image to Firebase Storage
        bucket = storage.bucket()
        blob = bucket.blob(image_filename)
        blob.upload_from_filename(image_filename)

        # Remove the locally saved image after uploading
        os.remove(image_filename)

        student_data = {
            "name": name,
            "major": major,
            "starting_year": starting_year,
            "standing": standing,
            "year": year,
            "total_attendance": 0,
            "last_attendance_time": last_attendance_time
        }
        ref.child(student_id).set(student_data)

        # Reset the captured_image variable
        captured_image = None

    ref = db.reference("Students")
    new_student_ref = ref.push()
    new_student_ref.set(student_data)

    messagebox.showinfo("Success", "Student registered successfully.")

def main():
    global name_entry, major_entry, starting_year_entry, standing_entry, year_entry, last_attendance_time_entry
    global captured_image  # Use the global captured_image variable

    root = tk.Tk()
    root.title("Student Registration")

    label = tk.Label(root, text="Fill in the details below to register a student:")
    label.pack(pady=10)

    name_label = tk.Label(root, text="Name:")
    name_label.pack()
    name_entry = tk.Entry(root)
    name_entry.pack()

    major_label = tk.Label(root, text="Major:")
    major_label.pack()
    major_entry = tk.Entry(root)
    major_entry.pack()

    starting_year_label = tk.Label(root, text="Starting Year:")
    starting_year_label.pack()
    starting_year_entry = tk.Entry(root)
    starting_year_entry.pack()

    standing_label = tk.Label(root, text="Standing:")
    standing_label.pack()
    standing_entry = tk.Entry(root)
    standing_entry.pack()

    year_label = tk.Label(root, text="Year:")
    year_label.pack()
    year_entry = tk.Entry(root)
    year_entry.pack()

    last_attendance_time_label = tk.Label(root, text="Last Attendance Time:")
    last_attendance_time_label.pack()
    last_attendance_time_entry = tk.Entry(root)
    last_attendance_time_entry.pack()

    capture_button = tk.Button(root, text="Capture Image", command=capture_image)
    capture_button.pack(pady=10)

    encode_button = tk.Button(root, text="Encode Students", command=encode_student)
    encode_button.pack(pady=10)

    register_button = tk.Button(root, text="Register", command=register_student)
    register_button.pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()