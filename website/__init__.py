from flask import Flask, render_template
import pymysql
import os
from dotenv import load_dotenv

load_dotenv()


hostname = os.getenv('DBHOSTNAME')
user = os.getenv('DBUSER')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')

db = pymysql.connections.Connection(
    host=hostname,
    user=user,
    password=password,
    database=database
)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    return app
