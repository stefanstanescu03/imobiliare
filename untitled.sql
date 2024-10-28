SELECT Utilizatori.Nume,
    Utilizatori.Prenume,
    Utilizatori.Telefon,
    Utilizatori.Email,
    Utilizatori.Data_nasterii,
    Agentii.Nume
FROM Utilizatori
    INNER JOIN Agentii ON Utilizatori.Email = 'fane@gmail.com'
    AND Utilizatori.AgentieID = Agentii.AgentieID;