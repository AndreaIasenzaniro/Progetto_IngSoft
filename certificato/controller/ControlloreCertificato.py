from datetime import datetime

class ControlloreCertificato():
    def __init__(self, certificato):
        self.model = certificato

    def isValido(self):
        return self.model is not None

    #restituisce la data di scadenza del certificato in una stringa
    def getScadenza(self):
        #print("TIMESTAMP: {}".format(self.model.scadenza))
        dataScadenza = datetime.fromtimestamp(self.model.scadenza)
        return "{}/{}/{}".format(dataScadenza.day, dataScadenza.month, dataScadenza.year)