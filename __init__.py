from flask import Flask
from flask_login import LoginManager
import mysql.connector

db = mysql.connector.connect(
        host="77.68.35.85",
        user="y13stephen",
        password="d#5G1vz90",
        database="y13stephen"
    )

def StartApp():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'StephenAccess85'


    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')


    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(UserID):
        from .models import User
        cursorObject = db.cursor()
        query = "SELECT * FROM NEA_Users_Table WHERE UserID = %s"
        data = (UserID,)
        cursorObject.execute(query, data)
        result = cursorObject.fetchone()
        if result is None:
            return None
        user = User(result[0], result[1], result[2], result[3])
        return user



    return app