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


def getProgramari(email):
    cursor = db.cursor()
    sql = '''SELECT Programari.Data_programarii, Proprietati.Denumire
            FROM Utilizatori
                INNER JOIN Programari ON Programari.UtilizatorID = Utilizatori.UtilizatorID
                INNER JOIN Proprietati ON Proprietati.ProprietateID = Programari.ProprietateID
            WHERE Utilizatori.email = %s'''
    result = cursor.execute(sql, (email))
    result = cursor.fetchall()
    cursor.close()

    programari = []

    for el in result:
        programari.append({
            'data': el[0],
            'denumire': el[1]
        })

    return programari


def getContracte(email):
    cursor = db.cursor()
    sql = '''SELECT Contracte.ContractID,
                Contracte.Data_incepere,
                Contracte.Data_incheiere,
                Contracte.Data_semnarii
            FROM Contracte
                INNER JOIN Utilizatori ON Utilizatori.UtilizatorID = Contracte.UtilizatorID
            WHERE Utilizatori.email = %s'''
    result = cursor.execute(sql, (email))
    result = cursor.fetchall()
    cursor.close

    contracte = []

    for el in result:
        contracte.append({
            'id': el[0],
            'data_incepere': el[1],
            'data_incheiere': el[2],
            'data_semnarii': el[3]
        })

    return contracte


def getInfo(id):
    cursor = db.cursor()
    sql = '''SELECT Contracte.ContractID,
        Contracte.Pret,
        Adrese.Judet,
        Adrese.Oras,
        Adrese.Scara,
        Adrese.Sector,
        Adrese.Strada,
        TipOferte.Denumire,
        Proprietati.Categorie,
        Proprietati.Etaj,
        Proprietati.Numar_adresa
    FROM Contracte
        INNER JOIN Proprietati ON Contracte.ProprietateID = Proprietati.ProprietateID
        INNER JOIN Adrese ON Adrese.AdresaID = Proprietati.AdresaID
        INNER JOIN TipOferte ON TipOferte.TipOfertaID = Contracte.TipOfertaID
    WHERE ContractID = %s'''
    result = cursor.execute(sql, (id))
    result = cursor.fetchall()
    cursor.close

    info = []

    for el in result:
        info.append({
            'id': el[0],
            'pret': el[1],
            'judet': el[2],
            'oras': el[3],
            'scara': el[4],
            'sector': el[5],
            'strada': el[6],
            'oferta': el[7],
            'categorie': el[8],
            'etaj': el[9],
            'numar_adresa': el[10]
        })

    return info
