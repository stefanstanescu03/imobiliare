from flask import Blueprint, render_template, request, make_response, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from .utils import getAgentieID, getAgentii, getToken, checkEmail

# Creează blueprint-ul pentru autentificare
auth = Blueprint('auth', __name__)


# Rute pentru autentificare utilizator
@auth.route('/login', methods=['GET', 'POST'])
def login():
    incorrect_password = False
    incorrect_email = False

    if request.method == 'POST':  # Dacă este trimis formularul
        email = request.form.get('email')
        password = request.form.get('password')

        # Verifică parola în baza de date
        sql = '''SELECT Parola FROM Utilizatori WHERE Email = %s'''
        cursor = db.cursor()
        cursor.execute(sql, (email))
        result = cursor.fetchone()
        cursor.close()

        if result is None:  # Dacă email-ul nu există
            incorrect_email = True
        else:
            result_password = result[0]
            # Dacă parola este corectă
            if check_password_hash(result_password, password):
                token = getToken(email)  # Generează un token
                # Redirecționează utilizatorul
                response = make_response(redirect(url_for('views.home')))
                response.set_cookie(
                    key="token",
                    value=token,
                    httponly=True,
                    max_age=24 * 60 * 60,
                    samesite="Strict"
                )  # Setează cookie-ul de autentificare
                return response
            else:
                incorrect_password = True  # Dacă parola este greșită

    return render_template('login.html', incorrect_password=incorrect_password, incorrect_email=incorrect_email, loggedIn=False)


# Rute pentru deconectare utilizator
@auth.route('/logout', methods=['GET'])
def logout():
    # Redirecționează utilizatorul la login
    response = make_response(redirect(url_for('auth.login')))
    response.delete_cookie('token')  # Șterge cookie-ul de autentificare
    return response


# Rute pentru înregistrare utilizator
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    agentii = getAgentii()  # Obține agențiile
    appear = False
    appearEmail = False

    if request.method == 'POST':  # Dacă este trimis formularul
        nume = request.form.get('nume')
        prenume = request.form.get('prenume')
        telefon = request.form.get('telefon')
        email = request.form.get('email')
        parola = request.form.get('parola')
        agentie = request.form.get('agentie')

        # Verifică dacă există câmpuri goale
        if nume == '' or prenume == '' or telefon == '' or email == '' or parola == '':
            appear = True
        else:
            if checkEmail(email) is False:  # Verifică dacă email-ul este valid
                appearEmail = True
            else:
                handleCreateAccount(nume, prenume, telefon,
                                    email, parola, agentie)  # Creează contul

    return render_template('signup.html', agentii=agentii, nr_agentii=len(agentii), appear=appear,
                           appearEmail=appearEmail, loggedIn=False)


# Funcție care gestionează crearea unui cont nou
def handleCreateAccount(nume, prenume, telefon, email, parola, agentie):
    parola_hash = generate_password_hash(parola)  # Criptează parola

    agentieID = getAgentieID(agentie)  # Obține ID-ul agenției

    cursor = db.cursor()

    if agentieID == None:  # Dacă nu există agenție
        sql = '''INSERT INTO Utilizatori (Nume, Prenume, Telefon, Email, Parola) VALUES (%s, %s, %s, %s, %s)'''
        cursor.execute(sql, (nume, prenume, telefon, email,
                       parola_hash))  # Adaugă utilizator fără agenție
    else:
        sql = '''INSERT INTO Utilizatori (Nume, Prenume, Telefon, Email, Parola, AgentieID) VALUES (%s, %s, %s, %s, %s, %s)'''
        cursor.execute(sql, (nume, prenume, telefon, email,
                       parola_hash, agentieID))  # Adaugă utilizator cu agenție

    db.commit()  # Salvează modificările
    cursor.close()  # Închide cursorul
