from flask import Blueprint, render_template, request, make_response, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .utils import getAgentieID, getAgentii, getToken, checkEmail


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    incorrect_password = False
    incorrect_email = False

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        sql = '''SELECT Parola FROM Utilizatori WHERE Email = %s'''
        cursor = db.cursor()
        cursor.execute(sql, (email))
        result = cursor.fetchone()
        cursor.close()

        if result is None:
            incorrect_email = True
        else:
            result_password = result[0]

            if check_password_hash(result_password, password):
                token = getToken(email)
                response = make_response(redirect(url_for('views.home')))
                response.set_cookie(
                    key="token",
                    value=token,
                    httponly=True,
                    max_age=24 * 60 * 60,
                    samesite="Strict"
                )
                return response
            else:
                incorrect_password = True

    return render_template('login.html', incorrect_password=incorrect_password, incorrect_email=incorrect_email, loggedIn=False)


@auth.route('/logout', methods=['GET'])
def logout():
    response = make_response(redirect(url_for('auth.login')))
    response.delete_cookie('token')
    return response


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    agentii = getAgentii()
    appear = False
    appearEmail = False

    if request.method == 'POST':
        nume = request.form.get('nume')
        prenume = request.form.get('prenume')
        telefon = request.form.get('telefon')
        email = request.form.get('email')
        parola = request.form.get('parola')
        agentie = request.form.get('agentie')

        if nume == '' or prenume == '' or telefon == '' or email == '' or parola == '':
            appear = True
        else:
            if checkEmail(email) is False:
                appearEmail = True
            else:
                handleCreateAccount(nume, prenume, telefon,
                                    email, parola, agentie)

    return render_template('signup.html', agentii=agentii, nr_agentii=len(agentii), appear=appear,
                           appearEmail=appearEmail, loggedIn=False)


def handleCreateAccount(nume, prenume, telefon, email, parola, agentie):
    parola_hash = generate_password_hash(parola)

    agentieID = getAgentieID(agentie)

    cursor = db.cursor()

    if agentieID == None:
        sql = '''INSERT INTO Utilizatori (Nume, Prenume, Telefon, Email, Parola) VALUES (%s, %s, %s, %s, %s)'''
        cursor.execute(sql, (nume, prenume, telefon,
                             email, parola_hash))
    else:
        sql = '''INSERT INTO Utilizatori (Nume, Prenume, Telefon, Email, Parola, AgentieID) VALUES (%s, %s, %s, %s, %s, %s)'''
        cursor.execute(sql, (nume, prenume, telefon,
                             email, parola_hash, agentieID))

    db.commit()
    cursor.close()
