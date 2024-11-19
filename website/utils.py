from . import db
from datetime import datetime, timedelta, timezone
import jwt
import json
import os


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


def getToken(email):
    sql1 = '''SELECT UtilizatorID, Nume, Prenume, Telefon, Email, Data_nasterii, AgentieID FROM Utilizatori
                WHERE Email = %s'''
    sql2 = '''SELECT Nume FROM Agentii WHERE AgentieID = %s'''

    cursor = db.cursor()
    cursor.execute(sql1, (email))
    result = cursor.fetchone()

    agentie = None
    if (result[6] != None):
        cursor.execute(sql2, (result[6]))
        result2 = cursor.fetchone()
        agentie = result2[0]

    data_nasterii = json.dumps(
        result[5], indent=4, sort_keys=True, default=str)
    if data_nasterii == 'null':
        data_nasterii = None

    payload = {
        'Id': result[0],
        'Nume': result[1],
        'Prenume': result[2],
        'Telefon': result[3],
        'Email': result[4],
        'Data_nasterii': data_nasterii,
        'Agentie': agentie,
        "exp": datetime.now(timezone.utc) + timedelta(hours=24)
    }

    token = jwt.encode(payload=payload, key=os.getenv('JWT_KEY'))
    cursor.close()

    return token


def checkEmail(email):
    cursor = db.cursor()
    sql = 'SELECT COUNT(*) FROM Utilizatori WHERE Email= %s'
    result = cursor.execute(sql, (email))
    result = cursor.fetchall()
    cursor.close()
    return result[0][0] == 0
