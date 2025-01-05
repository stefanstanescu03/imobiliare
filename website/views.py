from flask import Blueprint, render_template, request, jsonify, redirect, url_for
import jwt
import os
from . import db
from datetime import datetime, timedelta, timezone
from .utils import *
from .modifiers import *
import json

views = Blueprint('views', __name__)


# Ruta principală (pagina de home)
@views.route('/')
def home():
    loggedIn = False
    # Verificăm dacă există un token de autentificare în cookie
    token = request.cookies.get('token')
    if token is None:
        loggedIn = False
    else:
        loggedIn = True  # Dacă există token-ul, considerăm că utilizatorul este logat

    return render_template("./index.html", loggedIn=loggedIn)


# Ruta pentru pagina de cont a utilizatorului
@views.route('/account', methods=['GET', 'POST'])
def account():
    agentii = getAgentii()  # Obținem agențiile pentru a le afisa în form
    id = -1
    token = request.cookies.get('token')
    date = None
    # Verificăm utilizatorul este logat
    if token:
        data = jwt.decode(token, os.getenv("JWT_KEY"), algorithms=["HS256"])
        id = data["Id"]

        date = data["Data_nasterii"]
        if date:
            # Formatam data de nastere
            date = datetime.strptime(date, '"%Y-%m-%d"').strftime('%Y-%m-%d')

        # Obtinem programarile, contractele si anunturile utilizatorului
        programari = getProgramari(data['Email'])
        contracte = getContracte(data['Email'])
        anunturi = getAnunturiUtilizator(id)

    # Dacă este o cerere POST, utilizatorul dorește să își modifice datele
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


# Ruta responsabila cu modificarea unui contract
@views.route('/modificare-contract/id=<id>', methods=['GET', 'POST'])
def modificare_contract(id):
    contract = getContract(id)
    tipOferte = getTipOferte()

    # Verificam daca utilizatorul este logat
    token = request.cookies.get('token')
    if request.method == 'POST' and token is not None:
        fields = [
            'denumire', 'tip_oferta', 'pret', 'data_semnarii', 'data_incheiere',
            'data_incepere', 'categorie', 'compartimentare', 'nr_camere', 'nr_etaje',
            'suprafata', 'data_constructiei', 'judet', 'oras', 'sector', 'strada', 'scara', 'cod_postal',
            'etaj', 'numar_adresa', 'descriere', 'imagine'
        ]
        form_data = {field: request.form.get(
            field) or None for field in fields}

        print(form_data)

        # Verificam daca toate campurile obligatorii sunt completate
        if (form_data['denumire'] is None or form_data['tip_oferta'] is None or
            form_data['pret'] is None or form_data['data_semnarii'] is None or
            form_data['categorie'] is None or form_data['compartimentare'] is None or
            form_data['nr_camere'] is None or form_data['suprafata'] is None or
            form_data['data_constructiei'] is None or form_data['oras'] is None
            or form_data['strada'] is None or form_data['cod_postal'] is None or
                form_data['numar_adresa'] is None):
            incomplete_data = True
            return render_template('./modificare_contract.html', contract=contract,
                                   tipOferte=tipOferte, incomplete_data=incomplete_data)

        new_id = modifyAdresa(form_data['strada'], form_data['scara'], form_data['cod_postal'],
                              form_data['oras'], form_data['judet'], form_data['sector'], id)
        modifyProprietate(form_data.get('denumire'),
                          form_data.get('categorie'),
                          form_data.get('numar_adresa'),
                          form_data.get('compartimentare'),
                          form_data.get('nr_camere'),
                          form_data.get('nr_etaje'),
                          form_data.get('suprafata'),
                          form_data.get('etaj'),
                          form_data.get('data_constructiei'),
                          form_data.get('descriere'), id, new_id)
        modifyContract(form_data['tip_oferta'],
                       form_data.get('data_semnarii'),
                       form_data.get('data_incepere'),
                       form_data.get('data_incheiere'),
                       form_data.get('pret'), id)
        modifyImagine(form_data['imagine'], id)

    return render_template("./modificare_contract.html", contract=contract, tipOferte=tipOferte)


# Ruta pentru vizualizarea unui anunț (pentru identificare pasam ca variabila id-ul)
@views.route('/anunt/id=<id>', methods=['GET', 'POST'])
def anunt(id):
    loggedIn = False

    # Verificam daca utilizatorul este logat
    token = request.cookies.get('token')
    if token is None:
        loggedIn = False
    else:
        loggedIn = True
    anunt = getAnunt(id)  # Obtinem datele referitoare la anunt
    imagine = getImagine(id)  # Obtinem Imaginea asociata proprietatii
    facilitati = getFacilitati(id)  # Obtinem facilitatile proprietatii

    # In cazul unui request de tip POST, vom crea o programare de a viziona proprietatea
    if request.method == 'POST':
        data = request.form.get('programare')
        ora = request.form.get('time')
        proprietate_id = request.form.get('proprietateId')
        token = request.cookies.get('token')
        if token:
            account = jwt.decode(token, os.getenv(
                "JWT_KEY"), algorithms=["HS256"])
            id = account["Id"]
            programare = data + " " + ora  # Agregam data si ora
            handleAddProgramare(programare, id, proprietate_id)

    return render_template("./anunt.html", anunt=anunt, loggedIn=loggedIn,
                           facilitati=facilitati, imagine=imagine)


# Ruta pentru obținerea informațiilor unui contract
@views.route('/account/contract-info/<id>', methods=['POST'])
def info(id):
    infos = getInfo(id)
    infos = jsonify(infos)
    return infos


# Ruta responsabila cu modificarea detaliilor referitoare la o programare
@views.route('/account/modifica-programare', methods=['POST'])
def modifica_programare():
    if request.method == 'POST':
        data_programare = request.form.get('data_programarii')
        ora_programare = request.form.get('ora_programarii')
        id = request.form.get('programareId')
        handleUpdateProgramare(id, data_programare, ora_programare)

    return redirect('/account')


# Ruta responsabila cu stergerea unei programari
@views.route('/account/anulare-programare', methods=['POST'])
def anulareProgramare():
    if request.method == 'POST':
        id = request.form.get('id')
        handleDelete(id)
    return redirect('/account')


# Ruta responsabila cu stergerea unui anunt
@views.route('/account/stergere-anunt', methods=['POST'])
def stergere_anunt():
    if request.method == 'POST':
        id = request.form.get('anunt_id')
        handleDeleteAnunt(id)

    return redirect('/account')


# Ruta responsabila cu stergerea unui contract
@views.route('/account/stergere-contract', methods=['POST'])
def stergere_contract():
    if request.method == 'POST':
        id_contract = request.form.get("id_contract")
        id_proprietate = getProprietateFromContract(id_contract)

        # Stergem pe rand fiecare intrare care are legatura fie cu proprietatea
        # fie cu contractul pe care vrem sa-l stergem
        handleDeleteProgramari(id_proprietate)
        handleDeleteAnuntProprietate(id_proprietate)
        handleDeleteImagine(id_proprietate)
        handleDeleteFacilitai(id_proprietate)
        handleDeleteContract(id_contract)
        handleDeleteProprietate(id_proprietate)

    return redirect('/account')


# Ruta care returneaza anunturile care au imobile intr-o locatie
@views.route('/search/<locatie>', methods=['POST'])
def handleSearch(locatie):
    anunturi = getAnunturi(locatie)
    return anunturi


# Ruta care returneaza anunturile care au pretul mai mic decat pretul
# mediu al anunturilor din acea locatie
@views.route('/get-cheap/<locatie>', methods=['POST'])
def handleFilter(locatie):
    anunturi = getAnunturiIeftine(locatie)
    return anunturi


# Ruta responsabila cu publicarea unui anunt
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


# Ruta responsabila cu inregistrarea unui contract
@views.route('/inregistreaza-contract', methods=['GET', 'POST'])
def inregistreaza():
    facilitati = getFacilitatidb()
    tipOferte = getTipOferte()
    incomplete_data = False

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

        # Verificam daca toate campurile obligatorii sunt completate
        if (form_data['denumire'] is None or form_data['tip_oferta'] is None or
            form_data['pret'] is None or form_data['data_semnarii'] is None or
            form_data['categorie'] is None or form_data['compartimentare'] is None or
            form_data['nr_camere'] is None or form_data['suprafata'] is None or
            form_data['data_constructiei'] is None or form_data['oras'] is None
            or form_data['strada'] is None or form_data['cod_postal'] is None or
                form_data['numar_adresa'] is None or form_data['imagine'] is None):
            incomplete_data = True
            return render_template('./inregistrare.html', facilitati=facilitati,
                                   tipOferte=tipOferte, incomplete_data=incomplete_data)

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

    return render_template('./inregistrare.html', facilitati=facilitati,
                           tipOferte=tipOferte, incomplete_data=incomplete_data)
