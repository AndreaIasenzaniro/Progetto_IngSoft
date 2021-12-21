from datetime import datetime

class ControlloreCertificato():
    def __init__(self, certificato):
        self.model = certificato

    #ritorna true se si ha un certificato in corso di validità
    def isValido(self):
        return self.model is not None

    #restituisce la data di scadenza del certificato in una stringa
    def getScadenza(self):
        dataScadenza = datetime.fromtimestamp(self.model.scadenza)
        return "{}/{}/{}".format(dataScadenza.day, dataScadenza.month, dataScadenza.year)