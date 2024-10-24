-- @block
INSERT INTO TipOferte (Denumire)
VALUES ('Vanzare');
INSERT INTO TipOferte (Denumire)
VALUES ('Inchiriere');
-- @block
INSERT INTO Adrese (Strada, Scara, Cod_postal, Oras, Judet)
VALUES ('Lalelelor', 'B', '225200', 'Pitesti', 'Arges');
INSERT INTO Adrese (Strada, Cod_postal, Oras, Judet)
VALUES (
        'Fratii Buzesti',
        '384423',
        'Cluj-Napoca',
        'Cluj'
    );
INSERT INTO Adrese (Strada, Cod_postal, Oras, Judet)
VALUES (
        'Tudor Arghezi',
        '234222',
        'Targu Carbunesti',
        'Gorj'
    );
INSERT INTO Adrese (Strada, Scara, Cod_postal, Oras, Sector)
VALUES (
        'Progresului',
        'C',
        '225210',
        'Bucuresti',
        5
    );
INSERT INTO Adrese (Strada, Scara, Cod_postal, Oras, Sector)
VALUES ('Justitiei', 'D', '111222', 'Bucuresti', 1);
INSERT INTO Adrese (Strada, Cod_postal, Oras, Sector)
VALUES ('Crinul de padure', '211222', 'Bucuresti', 6);
-- @block
INSERT INTO Agentii (Nume, AdresaID, Numar_adresa, Email, Telefon)
VALUES (
        'King Imobiliare',
        3,
        12,
        'king@imobiliare.ro',
        '0773242938'
    );
INSERT INTO Agentii (Nume, AdresaID, Numar_adresa, Email, Telefon)
VALUES (
        'Alliance Rezidential',
        4,
        2,
        'alliance.rezidential@gmail.com',
        '0703142938'
    );
INSERT INTO Agentii (Nume, AdresaID, Numar_adresa, Telefon)
VALUES (
        'Habitat Group',
        4,
        10,
        '0713242938'
    );
-- @block
INSERT INTO Utilizatori (
        Nume,
        Prenume,
        Telefon,
        Email,
        Parola,
        Data_nasterii
    )
VALUES (
        'Popescu',
        'Ion',
        '0746359483',
        'ion@gmail.com',
        '1234',
        '2001/07/12'
    );
INSERT INTO Utilizatori (
        Nume,
        Prenume,
        Telefon,
        Email,
        Parola,
        Data_nasterii
    )
VALUES (
        'Alex',
        'Ionescu',
        '0746359481',
        'alx@gmail.com',
        'asdsd',
        '1990/07/12'
    );
INSERT INTO Utilizatori (
        Nume,
        Prenume,
        Telefon,
        Email,
        Parola,
        Data_nasterii
    )
VALUES (
        'Lorin',
        'Anghelescu',
        '0746359481',
        'asdsad@gmail.com',
        'asdsd23hfsd',
        '1990/07/12'
    );
INSERT INTO Utilizatori (
        Nume,
        Prenume,
        Telefon,
        Email,
        Parola
    )
VALUES (
        'Loren',
        'Gonzales',
        '0746359481',
        'loren@gmail.com',
        'dgiodfiogdhfg'
    );
INSERT INTO Utilizatori (
        Nume,
        Prenume,
        Telefon,
        Email,
        Parola,
        Data_nasterii
    )
VALUES (
        'Ghita',
        'Andreescu',
        '0746352281',
        'ghita@gmail.com',
        'dgiodfiogdhfg',
        '2003/01/12'
    );
INSERT INTO Utilizatori (
        Nume,
        Prenume,
        Telefon,
        Email,
        Parola
    )
VALUES (
        'Gogu',
        'Miclaus',
        '0788888888',
        'gogu@gmail.com',
        'bujie'
    );
INSERT INTO Utilizatori (
        Nume,
        Prenume,
        Telefon,
        Email,
        Parola,
        Data_nasterii,
        AgentieID
    )
VALUES (
        'Sebastian',
        'Dumitru',
        '0746359481',
        'Sebastian@imobiliare.ro',
        'dgiodfiogdhfg',
        '1999/01/12',
        1
    );
INSERT INTO Utilizatori (
        Nume,
        Prenume,
        Telefon,
        Email,
        Parola,
        Data_nasterii,
        AgentieID
    )
VALUES (
        'Mircea',
        'Pop',
        '0746359481',
        'mircea@gmail.ro',
        'fsdf',
        '2000/01/12',
        2
    );
INSERT INTO Utilizatori (
        Nume,
        Prenume,
        Telefon,
        Email,
        Parola,
        Data_nasterii,
        AgentieID
    )
VALUES (
        'Ionel',
        'Popa',
        '0716359481',
        'ionel@gmail.ro',
        'fsdsf',
        '2000/01/10',
        2
    );
INSERT INTO Utilizatori (
        Nume,
        Prenume,
        Telefon,
        Email,
        Parola,
        Data_nasterii,
        AgentieID
    )
VALUES (
        'Goga',
        'Marin',
        '0789098765',
        'goga@gmail.ro',
        'oooo',
        '2000/01/10',
        3
    );
-- @block
INSERT INTO Proprietati (
        Denumire,
        Categorie,
        AdresaID,
        Numar_adresa,
        Compartimentare,
        Numar_camere,
        Suprafata_utila,
        Etaj,
        Data_constructiei
    )
VALUES (
        'Prima inchiriere, 2 camere spatios si luminos',
        'Apartament',
        1,
        12,
        'Decomandat',
        2,
        60,
        8,
        "2017/02/23"
    );
INSERT INTO Proprietati (
        Denumire,
        Categorie,
        AdresaID,
        Numar_adresa,
        Compartimentare,
        Numar_camere,
        Suprafata_utila,
        Etaj,
        Data_constructiei
    )
VALUES (
        'Garsoniera Regie Residence',
        'Garsoniera',
        5,
        4,
        'Decomandat',
        1,
        40,
        1,
        "2023/02/23"
    );
INSERT INTO Proprietati (
        Denumire,
        Categorie,
        AdresaID,
        Numar_adresa,
        Compartimentare,
        Numar_camere,
        Suprafata_utila,
        Etaj,
        Data_constructiei
    )
VALUES (
        '2 camere vedere parcul Liniei',
        'Apartament',
        5,
        7,
        'Decomandat',
        2,
        69,
        4,
        "2022/12/23"
    );
INSERT INTO Proprietati (
        Denumire,
        Categorie,
        AdresaID,
        Numar_adresa,
        Numar_camere,
        Numar_etaje,
        Suprafata_utila,
        Data_constructiei,
        Descriere
    )
VALUES (
        'Casa Drumul Taberei',
        'Casa',
        6,
        14,
        5,
        1,
        140,
        "2015/12/23",
        'De inchiriat casa Drumul Taberei -  Valea Oltului, P + 1, suprafata utila 140 mp si suprafata teren 1400 mp, cu deschidere pe doua strazi,'
    );