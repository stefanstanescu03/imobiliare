from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import jwt
import os
from . import db
from datetime import datetime, timedelta, timezone
from .utils import *
import json

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

        programari = getProgramari(data['Email'])
        contracte = getContracte(data['Email'])

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

    return render_template("./account.html", data=data, agentii=agentii,
                           date=date, programari=programari, contracte=contracte)


@views.route('/anunt/id=<id>', methods=['GET', 'POST'])
def anunt(id):
    loggedIn = False
    token = request.cookies.get('token')
    if token is None:
        loggedIn = False
    else:
        loggedIn = True
    anunt = getAnunt(id)
    imagine = getImagine(id)
    facilitati = getFacilitati(id)

    if request.method == 'POST':
        data = request.form.get('programare')
        ora = request.form.get('time')
        proprietate_id = request.form.get('proprietateId')
        token = request.cookies.get('token')
        if token:
            account = jwt.decode(token, os.getenv(
                "JWT_KEY"), algorithms=["HS256"])
            id = account["Id"]
            programare = data + " " + ora
            print(programare, id, proprietate_id)
            handleAddProgramare(programare, id, proprietate_id)

    return render_template("./anunt.html", anunt=anunt, loggedIn=loggedIn,
                           facilitati=facilitati, imagine=imagine)


@views.route('/account/contract-info/<id>', methods=['POST'])
def info(id):
    infos = getInfo(id)
    infos = jsonify(infos)
    return infos


@views.route('/account/anulare-programare', methods=['POST'])
def anulareProgramare():
    if request.method == 'POST':
        id = request.form.get('id')
        handleDelete(id)
    return redirect('/account')


@views.route('/search/<locatie>', methods=['POST'])
def handleSearch(locatie):
    locatii = getAnunturi(locatie)
    print(locatii)
    return locatii


@views.route('/inregistreaza-contract', methods=['GET', 'POST'])
def publica():
    facilitati = getFacilitatidb()
    tipOferte = getTipOferte()

    if request.method == 'POST':
        fields = [
            'denumire', 'tip_oferta', 'pret', 'data_semnarii', 'data_incheiere',
            'data_incepere', 'categorie', 'compartimentare', 'nr_camere', 'nr_etaje',
            'suprafata', 'data', 'judet', 'oras', 'sector', 'strada', 'scara', 'cod_postal',
            'etaj', 'numar_adresa', 'descriere'
        ]
        form_data = {field: request.form.get(
            field) or None for field in fields}

        facilitati = request.form.get("facilitati")
        facilitati_list = []
        if facilitati:
            facilitati_list = eval(facilitati)

        for field, value in form_data.items():
            print(f"{field}: {value}")

        print(facilitati_list)

        token = request.cookies.get('token')
        if token:
            account = jwt.decode(token, os.getenv(
                "JWT_KEY"), algorithms=["HS256"])
            id = account["Id"]

            adresa_id = handleAddAddresa(form_data['strada'], form_data['scara'], form_data['cod_postal'],
                                         form_data['oras'], form_data['judet'], form_data['sector'])

            proprietate_id = handleAddProprietate(
                form_data.get('denumire'),
                form_data.get('categorie'),
                adresa_id,
                form_data.get('numar_adresa'),
                form_data.get('compartimentare'),
                form_data.get('nr_camere'),
                form_data.get('nr_etaje'),
                form_data.get('suprafata'),
                form_data.get('etaj'),
                form_data.get('data_constructiei'),
                form_data.get('descriere'))

            contract_id = handleAddContract(
                getTipOfertaId(form_data['tip_oferta']),
                id,
                proprietate_id,
                form_data.get('data_semnarii'),
                form_data.get('data_incepere'),
                form_data.get('data_incheiere'),
                form_data.get('pret')
            )
            for facilitate in facilitati_list:
                handleAddFacilitate(
                    proprietate_id, getFacilitateId(facilitate))

    return render_template('./inregistrare.html', facilitati=facilitati, tipOferte=tipOferte)


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
