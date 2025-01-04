from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import jwt
import os
from . import db
from datetime import datetime, timedelta, timezone
from .utils import *
from .modifiers import *
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
        anunturi = getAnunturiUtilizator(id)

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
                           date=date, programari=programari, contracte=contracte, anunturi=anunturi)


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


@views.route('/account/modifica-programare', methods=['POST'])
def modifica_programare():
    if request.method == 'POST':
        data_programare = request.form.get('data_programarii')
        ora_programare = request.form.get('ora_programarii')
        id = request.form.get('programareId')
        print(data_programare)
        print(ora_programare)
        print(id)
        handleUpdateProgramare(id, data_programare, ora_programare)

    return redirect('/account')


@views.route('/account/anulare-programare', methods=['POST'])
def anulareProgramare():
    if request.method == 'POST':
        id = request.form.get('id')
        handleDelete(id)
    return redirect('/account')


@views.route('/account/stergere-anunt', methods=['POST'])
def stergere_anunt():
    if request.method == 'POST':
        id = request.form.get('anunt_id')
        handleDeleteAnunt(id)

    return redirect('/account')


@views.route('/account/stergere-contract', methods=['POST'])
def stergere_contract():
    if request.method == 'POST':
        id_contract = request.form.get("id_contract")
        id_proprietate = getProprietateFromContract(id_contract)
        handleDeleteProgramari(id_proprietate)
        handleDeleteAnuntProprietate(id_proprietate)
        handleDeleteImagine(id_proprietate)
        handleDeleteFacilitai(id_proprietate)
        handleDeleteContract(id_contract)
        handleDeleteProprietate(id_proprietate)

    return redirect('/account')


@views.route('/search/<locatie>', methods=['POST'])
def handleSearch(locatie):
    locatii = getAnunturi(locatie)
    return locatii


@views.route('/publica-anunt', methods=['GET', 'POST'])
def publica():
    token = request.cookies.get('token')
    if token:
        account = jwt.decode(token, os.getenv(
            "JWT_KEY"), algorithms=["HS256"])
        id = account["Id"]
        tipOferte = getTipOferte()
        proprietati = getProprietati(id)

    if request.method == 'POST':
        proprietate_id = request.form.get('proprietate_id')
        pret = request.form.get('pret')
        tip_oferta = request.form.get('tip_oferta')

        handleAddAnunt(proprietate_id, pret, tip_oferta, id)

    return render_template('./publica.html', tipOferte=tipOferte, proprietati=proprietati)


@views.route('/inregistreaza-contract', methods=['GET', 'POST'])
def inregistreaza():
    facilitati = getFacilitatidb()
    tipOferte = getTipOferte()

    if request.method == 'POST':
        fields = [
            'denumire', 'tip_oferta', 'pret', 'data_semnarii', 'data_incheiere',
            'data_incepere', 'categorie', 'compartimentare', 'nr_camere', 'nr_etaje',
            'suprafata', 'data_constructiei', 'judet', 'oras', 'sector', 'strada', 'scara', 'cod_postal',
            'etaj', 'numar_adresa', 'descriere', 'imagine'
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

            handleAddImage(proprietate_id, form_data['imagine'])

            for facilitate in facilitati_list:
                handleAddFacilitate(
                    proprietate_id, getFacilitateId(facilitate))

    return render_template('./inregistrare.html', facilitati=facilitati, tipOferte=tipOferte)
