from datetime import datetime

class ControlloreAbbonamento():
    def __init__(self, abbonamento):
        self.model = abbonamento

    def is_abbonato(self):
        return self.model is not None

    #restituisce la data di scadenza dell'abbonamento in una stringa
    def get_scadenza_abbonamento(self):
        #print("TIMESTAMP: {}".format(self.model.scadenza))
        dataScadenza = datetime.fromtimestamp(self.model.scadenza)
        return "{}/{}/{}".format(dataScadenza.day, dataScadenza.month, dataScadenza.year)

    def get_tipo_abbonamento(self):
        return self.model.tipo

    def get_prezzo_abbonamento(self):
        return self.model.prezzo