import time

class Abbonamento():
    def __init__(self, scadenza, tipo, prezzo):
        self.scadenza = scadenza
        self.tipo = tipo
        self.prezzo = prezzo

    #verifica che un abbonamento sia in corso di validità
    def abb_in_corso(self):
        timestamp = int(time.time())
        return timestamp <= self.scadenza