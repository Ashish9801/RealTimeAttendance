import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
cred = credentials.Certificate("key1.json")
firebase_admin.initialize_app(cred,{
    'databaseURL': "https://attend-20d8b-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

ref=db.reference('Students')

data={
    "123454":
        {
            "Name": "Bindu Devi",
            "Major": "House Wife",
            "Starting-year": 2020,
            "total-attendance": 7,
            "standing": "12",
            "year": 4,
            "last_attendance_time": "2022-12-14 00:54:34"

        },
    "123455":
        {
            "Name": "Arun Kumar Singh",
            "Major": "BCCL Employee",
            "Starting-year": 2020,
            "total-attendance": 7,
            "standing": "12",
            "year": 4,
            "last_attendance_time": "2022-12-14 00:54:34"

        },
    "204101":
        {
            "Name": "Ashish Kumar Singh",
            "Major": "Computer Sci",
            "Starting-year": 2020,
            "total-attendance": 7,
            "standing": "12",
            "year": 4,
            "last_attendance_time": "2022-12-14 00:54:34"

        },
    "321654":
        {
            "Name": "Murtaza Hassan",
            "Major": "Robotics",
            "Starting-year": 2017,
            "total-attendance": 4,
            "standing": "6",
            "year": 4,
            "last_attendance_time": "2022-12-13 00:54:34"

        },
    "852741":
        {
            "Name": "Emily ",
            "Major": "Fashion",
            "Starting-year": 2020,
            "total-attendance": 4,
            "standing": "9",
            "year": 4,
            "last_attendance_time": "2022-12-12 00:54:34"

        },
    "963852":
        {
            "Name": "Elon Musk",
            "Major": "Mars colony",
            "Starting-year": 2018,
            "total-attendance": 6,
            "standing": "1",
            "year": 3,
            "last_attendance_time": "2022-12-12 00:54:34"

        }
}

for key, value in data.items():
    ref.child(key).set(value)
