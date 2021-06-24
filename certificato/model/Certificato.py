import time

class Certificato():
    def __init__(self, scadenza):
        self.scadenza = scadenza

    def inCorso(self):
        timestamp = int(time.time())
        return timestamp < self.scadenza