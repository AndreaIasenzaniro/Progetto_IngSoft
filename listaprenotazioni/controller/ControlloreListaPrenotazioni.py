from listaprenotazioni.model.ListaPrenotazioni import ListaPrenotazioni


class ControlloreListaPrenotazioni():
    def __init__(self):
        super(ControlloreListaPrenotazioni, self).__init__()
        self.model = ListaPrenotazioni()

    def aggiungi_prenotazione(self, prenotazione):
        self.model.aggiungi_prenotazione(prenotazione)

    def rimuovi_dalla_lista(self, prenotazione):
        self.model.rimuovi_dalla_lista(prenotazione)

    def ordina(self, lista):
        self.model.ordina_clienti(lista)

    def get_lista_prenotazioni(self):
        return self.model.get_lista_prenotazioni()

    def get_prenotazione_by_index(self, index):
        return self.model.get_prenotazione_by_index(index)

    def elimina_prenotazione_by_id(self, id):
        self.model.rimuovi_prenotazione_by_id(id)
        self.model.disdici_by_id(id)

    def save_data(self):
        self.model.save_data()