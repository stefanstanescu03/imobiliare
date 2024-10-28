from flask import Blueprint, render_template, request
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

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
                print("Logged in")
            else:
                incorrect_password = True

    return render_template('login.html', incorrect_password=incorrect_password, incorrect_email=incorrect_email)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    agentii = getAgentii()
    appear = False

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
            handleCreateAccount(nume, prenume, telefon, email, parola, agentie)

    return render_template('signup.html', agentii=agentii, nr_agentii=len(agentii), appear=appear)


def getAgentieID(nume):
    if nume == '---':
        return None

    cursor = db.cursor()
    sql = "SELECT AgentieID FROM Agentii WHERE Nume = %s"
    result = cursor.execute(sql, (nume))
    result = cursor.fetchone()
    cursor.close()

    return result[0]


def getAgentii():
    cursor = db.cursor()
    result = cursor.execute('SELECT Nume FROM Agentii')
    result = cursor.fetchall()

    agentii = ['---']

    for row in result:
        agentii.append(row[0])
    cursor.close()

    return agentii


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
