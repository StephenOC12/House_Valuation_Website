import mysql.connector
from flask_login import UserMixin,current_user
from flask import render_template



db = mysql.connector.connect(
        host="77.68.35.85",
        user="y13stephen",
        password="d#5G1vz90",
        database="y13stephen"
    )

class User(UserMixin):
    def __init__(self, UserID, UsernamePython, PhoneNumberPython, EmailAddressPython):
        self.UserID = UserID
        self.UsernamePython = UsernamePython
        self.EmailAddressPython = EmailAddressPython
        self.PhoneNumberPython = PhoneNumberPython


    def get_id(self):
        return (self.UserID)



cursorObject = db.cursor()

from .auth import UsernamePython

query = ("SELECT UserID, Username, Email_Address FROM NEA_Users_Table WHERE Username = %s ")
data = (UsernamePython,)
cursorObject.execute(query, data)


result = cursorObject.fetchone()

if result is not None:
    user = User(result[0], result[1], result[2], UsernamePython)
else:
    user = None

cursorObject.close()
db.close()







