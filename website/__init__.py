from flask import Flask, render_template
import pymysql
import os
from dotenv import load_dotenv

# Încarcă variabilele de mediu din fișierul .env
load_dotenv()

# Preia detaliile de conectare la baza de date din variabilele de mediu
hostname = os.getenv('DBHOSTNAME')
user = os.getenv('DBUSER')
password = os.getenv('PASSWORD')
database = os.getenv('DATABASE')

# Conectează-te la baza de date MySQL
db = pymysql.connections.Connection(
    host=hostname,
    user=user,
    password=password,
    database=database
)

# Creează aplicația Flask


def create_app():
    app = Flask(__name__)  # Inițializează aplicația Flask
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')  # Setează cheia secretă

    # Înregistrează blueprint-urile pentru views și auth
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/auth')

    return app  # Returnează aplicația configurată
