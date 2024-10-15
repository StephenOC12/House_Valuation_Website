from flask import Blueprint, render_template, request, flash, redirect
import re
from flask_login import login_user, login_required, logout_user, current_user
import mysql.connector

UsernamePython = ""

def restart():
    return redirect('/login')

restart()




auth = Blueprint('auth',__name__)

db = mysql.connector.connect(
        host="77.68.35.85",
        user="y13stephen",
        password="d#5G1vz90",
        database="y13stephen"
    )


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        global UsernamePython
        UsernamePython = request.form.get('UsernamePython')
        PasswordPython = request.form.get('PasswordPython')

        cursorObject = db.cursor()

        query = ("SELECT * FROM NEA_Users_Table WHERE username = %s AND password = %s")
        data = (UsernamePython, PasswordPython)

        cursorObject.execute(query, data)
        result = cursorObject.fetchone()
        if result:
            flash("Log in successful", category="success")
            from .models import User
            from .models import user
            login_user(user, remember=True)
            return redirect('/')
        else:
            flash("Log in failed", category="error")

    return render_template("login.html", user = current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/login')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        global UsernamePython
        EmailAddressPython = request.form.get('EmailAddressPython')
        PhoneNumberPython = request.form.get('PhoneNumberPython')
        UsernamePython = request.form.get('UsernamePython')
        PasswordPython = request.form.get('PasswordPython')
        PasswordAuth = request.form.get('PasswordAuth')

        EmailRegex = "^[A-Za-z0-9.-_]+@[A-Za-z0-9.]+\.[A-Za-z0-9.]{2,}$"
        PhoneNumberRegex = "^(07|447)[0-9]{9}$"
        PasswordRegex = "(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)(?=.*?[!?-_@*%':;`/<>])(?=^.{8,}$)"
        EmailResult = re.match(EmailRegex,EmailAddressPython)
        PhoneNumberResult = re.match(PhoneNumberRegex,PhoneNumberPython)
        PasswordResult = re.match(PasswordRegex,PasswordPython)

        def usernameTest():
            cursorObject = db.cursor()
            query = "SELECT * FROM NEA_Users_Table WHERE Username = %s"
            data = (UsernamePython,)
            cursorObject.execute(query, data)
            result = cursorObject.fetchone()
            if result:
                return True
            else:
                return False

        def emailTest():
            cursorObject = db.cursor()
            query = "SELECT * FROM NEA_Users_Table WHERE Email_Address = %s"
            data = (EmailAddressPython,)
            cursorObject.execute(query, data)
            result = cursorObject.fetchone()
            if result:
                return True
            else:
                return False

        def phoneTest():
            cursorObject = db.cursor()
            query = "SELECT * FROM NEA_Users_Table WHERE Phone_Number = %s"
            data = (PhoneNumberPython,)
            cursorObject.execute(query, data)
            result = cursorObject.fetchone()
            if result:
                return True
            else:
                return False


        if (usernameTest() == True):
            flash("Username already in use", category="error")
        elif (phoneTest() == True):
            flash("Phone number already in use", category="error")
        elif (emailTest() == True):
            flash("email address already in use", category="error")
        elif PasswordPython != PasswordAuth:
            flash("Passwords do not match", category="error")
        elif EmailResult is None:
            flash("Email Address is invalid", category="error")
        elif PhoneNumberResult is None:
            flash(EmailResult,category="error")
        elif PasswordResult is None:
            flash("Password is invalid", category="error")
        else:
            cursorObject = db.cursor()

            registerQuery = "INSERT INTO NEA_Users_Table(Username, Password, Email_Address, Phone_Number) VALUES (%s, %s, %s, %s)"
            val = (f"{UsernamePython}", f"{PasswordPython}", f"{EmailAddressPython}", f"{PhoneNumberPython}")
            cursorObject.execute(registerQuery, val)

            db.commit()

            db.close()


            from .models import User
            from .models import user



            login_user(user, remember=True)
            flash("Account registered", category="success")

            return redirect('/')


    return render_template("register.html", user = current_user)

