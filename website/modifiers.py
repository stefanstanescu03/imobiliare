from . import db
from datetime import datetime, timedelta, timezone
from .utils import *
import jwt
import json
import os


def handleUpdate(id, nume, prenume, telefon, email, data_nasterii, agentie_id):
    cursor = db.cursor()
    sql = '''UPDATE Utilizatori SET Nume = %s, Prenume = %s, Telefon = %s, Email = %s, Data_nasterii = %s, AgentieID = %s
        WHERE UtilizatorID = %s'''
    cursor.execute(sql, (nume, prenume, telefon, email,
                   data_nasterii, agentie_id, id))
    db.commit()
    cursor.close()


def handleAddProgramare(data_programarii, utilizator_id, proprietate_id):
    cursor = db.cursor()
    sql = '''INSERT INTO Programari (Data_programarii, UtilizatorID, ProprietateID)
        VALUES (%s, %s, %s)'''
    cursor.execute(sql, (data_programarii, utilizator_id, proprietate_id))
    db.commit()
    cursor.close()


def handleDelete(id):
    cursor = db.cursor()
    sql = '''DELETE FROM Programari WHERE ProgramareID = %s'''
    cursor.execute(sql, (id))
    db.commit()
    cursor.close()


def handleAddAddresa(strada, scara, cod_postal, oras, judet, sector):
    cursor = db.cursor()

    columns = ["Strada", "Scara", "Cod_postal", "Oras", "Judet", "Sector"]
    values = [strada, scara, cod_postal, oras, judet, sector]

    filtered_columns = [columns[i]
                        for i, value in enumerate(values) if value is not None]
    filtered_values = [value for value in values if value is not None]

    query = "SELECT AdresaID FROM Adrese WHERE " + \
        " AND ".join([f"{col} = %s" for col in filtered_columns])

    if filtered_values:
        cursor.execute(query, tuple(filtered_values))
        result = cursor.fetchone()

        if result:
            cursor.close()
            return result[0]

    insert_query = f"INSERT INTO Adrese ({', '.join(filtered_columns)}) VALUES ({
        ', '.join(['%s'] * len(filtered_values))})"

    cursor.execute(insert_query, tuple(filtered_values))
    db.commit()

    new_id = cursor.lastrowid
    cursor.close()
    return new_id


def handleAddProprietate(denumire, categorie, adresa_id, numar_adresa,
                         compartimentare, numar_camere, numar_etaje,
                         suprafata_utila, etaj, data_constructiei, descriere):
    cursor = db.cursor()
    values = [denumire, categorie, adresa_id, numar_adresa, compartimentare,
              numar_camere, numar_etaje, suprafata_utila, etaj, data_constructiei, descriere]
    columns = ["Denumire", "Categorie", "AdresaID", "Numar_adresa", "Compartimentare",
               "Numar_camere", "Numar_etaje", "Suprafata_utila", "Etaj", "Data_constructiei", "Descriere"]

    filtered_columns = [col for col, val in zip(
        columns, values) if val is not None]
    filtered_values = [val for val in values if val is not None]

    column_str = ", ".join(filtered_columns)
    value_placeholder_str = ", ".join(["%s"] * len(filtered_values))

    insert_query = f"INSERT INTO Proprietati ({column_str}) VALUES ({
        value_placeholder_str})"
    cursor.execute(insert_query, filtered_values)

    db.commit()

    new_id = cursor.lastrowid
    cursor.close()
    return new_id


def handleAddContract(tip_oferta_id, utilizator_id, proprietate_id,
                      data_semnarii, data_incepere, data_incheiere, pret):
    cursor = db.cursor()

    columns = ['TipOfertaID', 'UtilizatorID', 'ProprietateID',
               'Data_semnarii', 'Data_incepere', 'Data_incheiere', 'Pret']
    values = [tip_oferta_id, utilizator_id, proprietate_id,
              data_semnarii, data_incepere, data_incheiere, pret]

    filtered_columns = [col for col, val in zip(
        columns, values) if val is not None]
    filtered_values = [val for val in values if val is not None]

    query = f"INSERT INTO Contracte ({', '.join(filtered_columns)}) VALUES ({
        ', '.join(['%s'] * len(filtered_values))})"

    cursor.execute(query, tuple(filtered_values))
    db.commit()

    new_id = cursor.lastrowid
    cursor.close()

    return new_id


def handleAddFacilitate(proprietate_id, facilitate_id):
    cursor = db.cursor()
    cursor.execute('INSERT INTO Detalii_suplimentare (ProprietateID, FacilitateID) VALUES (%s, %s)',
                   (proprietate_id, facilitate_id))
    db.commit()
    cursor.close()


def handleAddImage(proprietate_id, path):
    cursor = db.cursor()
    cursor.execute(
        '''INSERT INTO Imagini (Path, ProprietateID) VALUES (%s, %s)''', (path, proprietate_id))
    db.commit()
    cursor.close()


def handleAddAnunt(proprietate_id, pret, tip_oferta, utilizator_id):
    tip_oferta_id = getTipOfertaId(tip_oferta)
    data_publicarii = datetime.now().strftime("%Y-%m-%d")

    cursor = db.cursor()
    cursor.execute('''INSERT INTO Anunturi (TipOfertaID, Data_publicarii, ProprietateID, UtilizatorID, Pret)
                   VALUES (%s, %s, %s, %s, %s)''', (tip_oferta_id, data_publicarii, proprietate_id, utilizator_id, pret))

    db.commit()
    cursor.close()


def handleUpdateProgramare(id, data_programare, ora_programare):
    programare = data_programare + " " + ora_programare
    cursor = db.cursor()
    cursor.execute('''UPDATE Programari SET Data_programarii = %s
                   WHERE ProgramareID = %s''', (programare, id))
    db.commit()
    cursor.close()


def handleDeleteAnunt(id):
    cursor = db.cursor()
    cursor.execute('''DELETE FROM Anunturi WHERE AnuntID = %s''', (id))
    db.commit()
    cursor.close()
