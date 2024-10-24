-- @block
CREATE TABLE Utilizatori (
    UtilizatorID BIGINT NOT NULL AUTO_INCREMENT,
    Nume VARCHAR(50) NOT NULL,
    Prenume VARCHAR(50) NOT NULL,
    Telefon CHAR(10) NOT NULL,
    Email VARCHAR(50) NOT NULL,
    Parola VARCHAR(50) NOT NULL,
    Data_nasterii DATE,
    AgentieID BIGINT,
    PRIMARY KEY (UtilizatorID)
);
-- @block
CREATE TABLE Agentii (
    AgentieID BIGINT NOT NULL AUTO_INCREMENT,
    Nume VARCHAR(50) NOT NULL,
    AdresaID BIGINT NOT NULL,
    Numar_adresa INT NOT NULL,
    Email VARCHAR(50),
    Telefon CHAR(10) NOT NULL,
    PRIMARY KEY (AgentieID)
);
-- @block
ALTER TABLE Utilizatori
ADD CONSTRAINT AgentieID FOREIGN KEY (AgentieID) REFERENCES Agentii(AgentieID);
-- @block
CREATE TABLE Adrese (
    AdresaID BIGINT NOT NULL AUTO_INCREMENT,
    Strada VARCHAR(50) NOT NULL,
    Scara CHAR(1),
    Cod_postal VARCHAR(50) NOT NULL,
    Oras VARCHAR(50) NOT NULL,
    Judet VARCHAR(50),
    Sector INT,
    PRIMARY KEY (AdresaID)
);
-- @block
ALTER TABLE Agentii
ADD CONSTRAINT AdresaID FOREIGN KEY (AdresaID) REFERENCES Adrese(AdresaID);
-- @block
CREATE TABLE Proprietati (
    ProprietateID BIGINT NOT NULL AUTO_INCREMENT,
    Denumire VARCHAR(50) NOT NULL,
    Categorie VARCHAR(50) NOT NULL,
    AdresaID BIGINT NOT NULL,
    Numar_adresa INT NOT NULL,
    Compartimentare VARCHAR(50),
    Numar_camere INT NOT NULL,
    Numar_etaje INT,
    Suprafata_utila INT NOT NULL,
    Etaj INT,
    Data_constructiei date,
    Descriere VARCHAR(255),
    PRIMARY KEY (ProprietateID),
    FOREIGN KEY (AdresaID) REFERENCES Adrese(AdresaID),
    CHECK (
        Categorie IN ('Apartament', 'Garsoniera', 'Casa')
    )
);
-- @block
CREATE TABLE Programari(
    ProgramareID BIGINT NOT NULL AUTO_INCREMENT,
    Data_programarii DATETIME NOT NULL,
    UtilizatorID BIGINT NOT NULL,
    ProprietateID BIGINT NOT NULL,
    PRIMARY KEY (ProgramareID),
    FOREIGN KEY (UtilizatorID) REFERENCES Utilizatori(UtilizatorID),
    FOREIGN KEY (ProprietateID) REFERENCES Proprietati(ProprietateID)
);
-- @block
CREATE TABLE Imagini(
    ImagineID BIGINT NOT NULL AUTO_INCREMENT,
    Path VARCHAR(50) NOT NULL,
    ProprietateID BIGINT NOT NULL,
    PRIMARY KEY (ImagineID),
    FOREIGN KEY (ProprietateID) REFERENCES Proprietati(ProprietateID)
);
-- @block
CREATE TABLE Facilitati(
    FacilitateID BIGINT NOT NULL AUTO_INCREMENT,
    Denumire VARCHAR(50) NOT NULL,
    PRIMARY KEY (FacilitateID)
);
-- @block
CREATE TABLE Detalii_suplimentare(
    id BIGINT NOT NULL AUTO_INCREMENT,
    ProprietateID BIGINT NOT NULL,
    FacilitateID BIGINT NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (ProprietateID) REFERENCES Proprietati(ProprietateID),
    FOREIGN KEY (FacilitateID) REFERENCES Facilitati(FacilitateID)
);
-- @block
CREATE TABLE TipOferte(
    TipOfertaID BIGINT NOT NULL AUTO_INCREMENT,
    Denumire VARCHAR(50) NOT NULL,
    PRIMARY KEY (TipOfertaID)
) -- @block
CREATE TABLE Anunturi(
    AnuntID BIGINT NOT NULL AUTO_INCREMENT,
    TipOfertaID BIGINT NOT NULL,
    Data_publicarii VARCHAR(50) NOT NULL,
    ProprietateID BIGINT NOT NULL,
    UtilizatorID BIGINT NOT NULL,
    Pret DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (AnuntID),
    FOREIGN KEY (TipOfertaID) REFERENCES TipOferte(TipOfertaID),
    FOREIGN KEY (ProprietateID) REFERENCES Proprietati(ProprietateID),
    FOREIGN KEY (UtilizatorID) REFERENCES Utilizatori(UtilizatorID)
);
-- @block
CREATE TABLE Contracte(
    ContractID BIGINT NOT NULL AUTO_INCREMENT,
    TipOfertaID BIGINT NOT NULL,
    UtilizatorID BIGINT NOT NULL,
    ProprietateID BIGINT NOT NULL,
    Data_semnarii DATE NOT NULL,
    Data_incepere DATE,
    Data_incheiere DATE,
    Pret DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (ContractID),
    FOREIGN KEY (TipOfertaID) REFERENCES TipOferte(TipOfertaID),
    FOREIGN KEY (UtilizatorID) REFERENCES Utilizatori(UtilizatorID),
    FOREIGN KEY (ProprietateID) REFERENCES Proprietati(ProprietateID)
);
-- @block
ALTER TABLE Adrese
MODIFY COLUMN Judet VARCHAR(50);