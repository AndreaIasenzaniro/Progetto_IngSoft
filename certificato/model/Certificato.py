import time

class Certificato():
    def __init__(self, scadenza):
        self.scadenza = scadenza

    #verifica che un certificato sia in corso di validità
    def inCorso(self):
        timestamp = int(time.time())
        return timestamp < self.scadenza