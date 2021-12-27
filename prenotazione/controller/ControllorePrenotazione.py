from prenotazione.model.Prenotazione import *

class ControllorePrenotazione():
    def __init__(self, prenotazione):
        # il model è della prenotazione che viene passata
        self.model = prenotazione

    def get_id_prenotazione(self):
        return self.model.id

    def get_nome(self):
        return self.model.nome

    def get_cognome(self):
        return self.model.cognome

    def get_documento(self):
        return self.model.documento

    def get_campo_tipo(self):
        return self.model.campo.tipo

    def get_campo_num(self):
        return self.model.campo.numero

    def get_data_prenotazione(self):
        return self.model.data

    def get_ora_inizio(self):
        return self.model.ora_inizio

    def get_ora_fine(self):
        return self.model.ora_fine

    def verifica_stato(self):
        return self.model.verifica_stato

    def prezzi_campi(self):
        return self.model.prezzi_campi()