SELECT Contracte.Pret,
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
WHERE ContractID = 4;