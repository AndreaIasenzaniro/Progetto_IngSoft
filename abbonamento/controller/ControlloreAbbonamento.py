from datetime import datetime

class ControlloreAbbonamento():
    def __init__(self, abbonamento):
        self.model = abbonamento

    #ritorna true se si ha un abbonamento in corso di validità
    def is_abbonato(self):
        return self.model is not None

    #restituisce la data di scadenza dell'abbonamento in una stringa
    def get_scadenza_abbonamento(self):
        dataScadenza = datetime.fromtimestamp(self.model.scadenza)
        return "{}/{}/{}".format(dataScadenza.day, dataScadenza.month, dataScadenza.year)

    #restituisce il tipo di abbonamento tramite il model
    def get_tipo_abbonamento(self):
        return self.model.tipo

    #restituisce il prezzo dell'abbonamento tramite il model
    def get_prezzo_abbonamento(self):
        return self.model.prezzo