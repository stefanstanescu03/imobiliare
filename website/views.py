from flask import Blueprint, render_template, request
import jwt
import os
from . import db
from datetime import datetime, timedelta, timezone
from .utils import getAgentieID, getAgentii

views = Blueprint('views', __name__)


@views.route('/')
def home():
    loggedIn = False
    token = request.cookies.get('token')
    if token is None:
        loggedIn = False
    else:
        loggedIn = True
    return render_template("./index.html", loggedIn=loggedIn)


@views.route('/account', methods=['GET', 'POST'])
def account():
    agentii = getAgentii()
    id = -1
    token = request.cookies.get('token')
    date = None
    if token:
        data = jwt.decode(token, os.getenv("JWT_KEY"), algorithms=["HS256"])
        id = data["Id"]

        date = data["Data_nasterii"]
        if date:
            date = datetime.strptime(date, '"%Y-%m-%d"').strftime('%Y-%m-%d')

    if request.method == 'POST':
        nume = request.form.get('nume')
        prenume = request.form.get('prenume')
        telefon = request.form.get('telefon')
        email = request.form.get('email')
        data_nasterii = request.form.get('data_nasterii')
        agentie_id = getAgentieID(request.form.get('agentie'))
        if data_nasterii == '':
            data_nasterii = None
        handleUpdate(id, nume, prenume, telefon,
                     email, data_nasterii, agentie_id)

    return render_template("./account.html", data=data, agentii=agentii, date=date)


def handleUpdate(id, nume, prenume, telefon, email, data_nasterii, agentie_id):
    cursor = db.cursor()
    sql = '''UPDATE Utilizatori SET Nume = %s, Prenume = %s, Telefon = %s, Email = %s, Data_nasterii = %s, AgentieID = %s
        WHERE UtilizatorID = %s'''
    cursor.execute(sql, (nume, prenume, telefon, email,
                   data_nasterii, agentie_id, id))
    db.commit()
    cursor.close()
