from firebase_admin import db
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    "databaseURL":"https://schoolattendance-f10d2-default-rtdb.firebaseio.com/"
})


ref = db.reference('Students')

data = {
    "321654":
        {
            "name": "Alex Murimi",
            "major": "Computer Science",
            "starting_year": 2023,
            "total_attendance": 7,
            "standing": "G",
            "year": 4,
            "last_attendance_time": "2023-08-01 03:23:34"
        },
    "852741":
        {
            "name": "Emly Blunt",
            "major": "Economics",
            "starting_year": 2021,
            "total_attendance": 12,
            "standing": "B",
            "year": 1,
            "last_attendance_time": "2023-08-01 03:23:34"
        },
    "963852":
        {
            "name": "Elon Musk",
            "major": "Physics",
            "starting_year": 2020,
            "total_attendance": 7,
            "standing": "G",
            "year": 2,
            "last_attendance_time": "2023-08-01 03:23:34"
        }
}

for key, value in data.items():
    ref.child(key).set(value)