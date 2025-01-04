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


def getTipOferte():
    cursor = db.cursor()
    result = cursor.execute('SELECT Denumire FROM TipOferte')
    result = cursor.fetchall()

    tipuri = []

    for row in result:
        tipuri.append(row[0])
    cursor.close()

    return tipuri


def getFacilitatidb():
    cursor = db.cursor()
    result = cursor.execute('SELECT Denumire FROM Facilitati')
    result = cursor.fetchall()

    facilitati = []

    for row in result:
        facilitati.append(row[0])
    cursor.close()

    return facilitati


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
    sql = '''SELECT Programari.Data_programarii,
            Proprietati.Denumire,
            Programari.ProgramareID,
            Adrese.Strada,
            Adrese.Scara,
            Adrese.Oras,
            Adrese.Judet,
            Adrese.Sector,
            Proprietati.Numar_adresa,
            Proprietati.Etaj
        FROM Utilizatori
            INNER JOIN Programari ON Programari.UtilizatorID = Utilizatori.UtilizatorID
            INNER JOIN Proprietati ON Proprietati.ProprietateID = Programari.ProprietateID
            INNER JOIN Adrese ON Proprietati.AdresaID = Adrese.AdresaID
        WHERE Utilizatori.email = %s;'''
    result = cursor.execute(sql, (email))
    result = cursor.fetchall()
    cursor.close()

    programari = []

    for el in result:
        programari.append({
            'data': el[0],
            'denumire': el[1],
            'id': el[2],
            'strada': el[3],
            'scara': el[4],
            'oras': el[5],
            'judet': el[6],
            'sector': el[7],
            'numar_adresa': el[8],
            'etaj': el[9]
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
    cursor.close()

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
    cursor.close()

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


def getAnunturi(locatie):
    cursor = db.cursor()
    sql = '''SELECT Anunturi.AnuntID, Proprietati.Denumire, TipOferte.Denumire
            FROM Proprietati
            INNER JOIN Anunturi ON Proprietati.ProprietateID = Anunturi.ProprietateID
            INNER JOIN TipOferte ON TipOferte.TipOfertaID = Anunturi.TipOfertaID
            INNER JOIN Adrese ON Adrese.AdresaID = Proprietati.AdresaID
            WHERE Adrese.Oras = %s'''
    result = cursor.execute(sql, (locatie))
    result = cursor.fetchall()
    cursor.close

    anunturi = []
    for el in result:
        anunturi.append({
            'id': el[0],
            'denumire': el[1],
            'oferta': el[2]
        })

    return anunturi


def getAnunturiUtilizator(id):
    cursor = db.cursor()
    cursor.execute('''SELECT Anunturi.AnuntID,
                    Proprietati.Denumire
                    FROM Anunturi
                        INNER JOIN Proprietati ON Anunturi.ProprietateID = Proprietati.ProprietateID
                        INNER JOIN Utilizatori ON Utilizatori.UtilizatorID = Anunturi.UtilizatorID
                    WHERE Utilizatori.UtilizatorID = %s''', (id))
    result = cursor.fetchall()
    cursor.close

    anunturi = []
    for el in result:
        anunturi.append({
            'id': el[0],
            'denumire': el[1],
        })

    return anunturi


def getAnunt(id):
    cursor = db.cursor()
    sql = '''SELECT Anunturi.AnuntID,
        TipOferte.Denumire,
        Anunturi.Data_publicarii,
        Anunturi.Pret,
        Proprietati.Denumire,
        Proprietati.Categorie,
        Proprietati.Numar_adresa,
        Proprietati.Compartimentare,
        Proprietati.Numar_camere,
        Proprietati.Numar_etaje,
        Proprietati.Suprafata_utila,
        Proprietati.Etaj,
        Proprietati.Data_constructiei,
        Proprietati.Descriere,
        Adrese.Strada,
        Adrese.Scara,
        Adrese.Cod_postal,
        Adrese.Oras,
        Adrese.Judet,
        Adrese.Sector,
        Proprietati.ProprietateID
        FROM Proprietati
        INNER JOIN Anunturi ON Proprietati.ProprietateID = Anunturi.ProprietateID
        INNER JOIN TipOferte ON TipOferte.TipOfertaID = Anunturi.TipOfertaID
        INNER JOIN Adrese ON Adrese.AdresaID = Proprietati.AdresaID
        WHERE Anunturi.AnuntID = %s'''
    result = cursor.execute(sql, (id))
    result = cursor.fetchall()
    cursor.close()

    anunt = {
        'id': result[0][0],
        'oferta': result[0][1],
        'data_publicarii': result[0][2],
        'pret (EUR)': result[0][3],
        'denumire': result[0][4],
        'categorie': result[0][5],
        'numar_adresa': result[0][6],
        'compartimentare': result[0][7],
        'numar_camere': result[0][8],
        'numar_etaje': result[0][9],
        'suprafata_utila (mp)': result[0][10],
        'etaj': result[0][11],
        'data_constructiei': result[0][12],
        'descriere': result[0][13],
        'strada': result[0][14],
        'scara': result[0][15],
        'cod_postal': result[0][16],
        'oras': result[0][17],
        'judet': result[0][18],
        'sector': result[0][19],
        'proprietateId': result[0][20]
    }
    return anunt


def getFacilitati(id):
    cursor = db.cursor()
    sql = '''SELECT Facilitati.Denumire
            FROM Facilitati
                INNER JOIN Detalii_suplimentare ON Detalii_suplimentare.FacilitateID = Facilitati.FacilitateID
                INNER JOIN Proprietati ON Detalii_suplimentare.ProprietateID = Proprietati.ProprietateID
                INNER JOIN Anunturi ON Anunturi.ProprietateID = Proprietati.ProprietateID
            WHERE Anunturi.AnuntID = %s'''
    result = cursor.execute(sql, (id))
    result = cursor.fetchall()
    cursor.close()

    facilitati = []
    for facilitate in result:
        facilitati.append(facilitate[0])

    return facilitati


def getImagine(id):
    cursor = db.cursor()
    sql = '''SELECT Imagini.Path
            FROM Imagini
                INNER JOIN Proprietati ON Imagini.ProprietateID = Proprietati.ProprietateID
                INNER JOIN Anunturi ON Anunturi.ProprietateID = Proprietati.ProprietateID
            WHERE Anunturi.AnuntID = %s'''
    result = cursor.execute(sql, (id))
    result = cursor.fetchall()
    cursor.close()
    imagine = result[0][0]
    return imagine


def getTipOfertaId(Denumire):
    cursor = db.cursor()
    result = cursor.execute(
        'SELECT TipOfertaID FROM TipOferte WHERE Denumire=%s', (Denumire))
    result = cursor.fetchall()
    cursor.close()
    return result[0][0]


def getFacilitateId(Denumire):
    cursor = db.cursor()
    result = cursor.execute(
        'SELECT FacilitateID FROM Facilitati WHERE Denumire=%s', (Denumire))
    result = cursor.fetchall()
    cursor.close()

    return result[0][0]


def getProprietati(id):
    cursor = db.cursor()
    result = cursor.execute('''SELECT Proprietati.ProprietateID, Proprietati.Denumire
                            FROM Proprietati
                            INNER JOIN Contracte ON Contracte.ProprietateID = Proprietati.ProprietateID
                            WHERE Contracte.UtilizatorID=%s''', (id))
    result = cursor.fetchall()
    cursor.close()

    proprietati = []
    for el in result:
        proprietati.append({
            'id': el[0],
            'denumire': el[1]
        })

    return proprietati


def getProprietateFromContract(id):
    cursor = db.cursor()
    cursor.execute(
        '''SELECT ProprietateID FROM Contracte WHERE ContractID = %s''', (id))
    result = cursor.fetchall()
    cursor.close()
    return result[0][0]


def handleDeleteAnuntProprietate(id):
    cursor = db.cursor()
    cursor.execute('''DELETE FROM Anunturi WHERE ProprietateID = %s''', (id))
    db.commit()
    cursor.close()


def handleDeleteImagine(id):
    cursor = db.cursor()
    cursor.execute('''DELETE FROM Imagini WHERE ProprietateID = %s''', (id))
    db.commit()
    cursor.close()


def handleDeleteFacilitai(id):
    cursor = db.cursor()
    cursor.execute(
        '''DELETE FROM Detalii_suplimentare WHERE ProprietateID = %s''', (id))
    db.commit()
    cursor.close()


def handleDeleteContract(id):
    cursor = db.cursor()
    cursor.execute('''DELETE FROM Contracte WHERE ContractID = %s''', (id))
    db.commit()
    cursor.close()


def handleDeleteProgramari(id):
    cursor = db.cursor()
    cursor.execute('''DELETE FROM Programari WHERE ProprietateID = %s''', (id))
    db.commit()
    cursor.close()


def handleDeleteProprietate(id):
    cursor = db.cursor()

    cursor.execute('''SELECT COUNT(*)
                    FROM Proprietati
                    WHERE AdresaID = (
                        SELECT AdresaID
                        FROM Proprietati
                        WHERE ProprietateID = %s
                    );''', (id))

    result = cursor.fetchall()
    total = result[0][0]

    cursor.execute(
        '''SELECT AdresaID FROM Proprietati WHERE ProprietateID = %s''', (id))
    result = cursor.fetchall()
    adresa_id = result[0][0]

    cursor.execute(
        '''DELETE FROM Proprietati WHERE ProprietateID = %s''', (id))
    db.commit()

    if total == 1:
        cursor.execute(
            '''DELETE FROM Adrese WHERE AdresaID = %s''', (adresa_id))
        db.commit()

    cursor.close()
