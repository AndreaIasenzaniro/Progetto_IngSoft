import time

class Abbonamento():
    def __init__(self, scadenza, tipo, prezzo):
        self.scadenza = scadenza
        self.tipo = tipo
        self.prezzo = prezzo

    def abb_in_corso(self):
        timestamp = int(time.time())
        return timestamp <= self.scadenza

    '''def assegna_prezzo(self):
        if self.tipo == "Giornaliero":
            return 8
        if self.tipo == "Mensile":
            return 35
        if self.tipo == "Trimestrale":
            return 90
        if self.tipo == "Annuale":
            return 360'''