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
    sql = '''SELECT Utilizatori.UtilizatorID,
                Utilizatori.Nume,
                Utilizatori.Prenume,
                Utilizatori.Telefon,
                Utilizatori.Email,
                Utilizatori.Data_nasterii,
                Agentii.Nume
            FROM Utilizatori
                INNER JOIN Agentii ON Utilizatori.Email = %s
                AND Utilizatori.AgentieID = Agentii.AgentieID;'''

    cursor = db.cursor()
    cursor.execute(sql, (email))
    result = cursor.fetchone()
    cursor.close()

    payload = {
        'Id': result[0],
        'Nume': result[1],
        'Prenume': result[2],
        'Telefon': result[3],
        'Email': result[4],
        'Data_nasterii': json.dumps(result[5], indent=4, sort_keys=True, default=str),
        'Agentie': result[6],
        "exp": datetime.now(timezone.utc) + timedelta(hours=24)
    }

    token = jwt.encode(payload=payload, key=os.getenv('JWT_KEY'))

    return token
