import os
import pickle


class ListaPrenotazioni():
    def __init__(self):
        super(ListaPrenotazioni, self).__init__()
        # definisco una lista vuota per le prenotazioni
        self.lista_prenotazioni = []
        # se presente il file che contiene i dati della lista, lo apro e la popolo
        if os.path.isfile('listaprenotazioni/data/lista_prenotazioni_salvata.pickle'):
            with open('listaprenotazioni/data/lista_prenotazioni_salvata.pickle', 'rb') as f:
                self.lista_prenotazioni = pickle.load(f)

    def aggiungi_prenotazione(self, prenotazione):
        self.lista_prenotazioni.append(prenotazione)

    def rimuovi_dalla_lista(self, prenotazione):
        self.lista_prenotazioni.remove(prenotazione)

    # funzione che ordina la lista delle prenotazioni per ora di inizio
    def ordina_lista(self, lista):
        lista.sort(key=lambda x:x.ora_inizio, reverse = False)

    # funzione che rimuove una prenotazione dalla lista dato il suo id
    def rimuovi_prenotazione_by_id(self, id):
        # scorre la lista finchè gli id non corrispondono
        for prenotazione in self.lista_prenotazioni:
            if prenotazione.id == id:
                self.lista_prenotazioni.remove(prenotazione)
                return True
        return False

    # funzione che ritorna la prenotaizone all'indice dato
    def get_prenotazione_by_index(self, index):
        return self.lista_prenotazioni[index]

    # funzione che ritorna la lista delle prenotazioni
    def get_lista_prenotazioni(self):
        return self.lista_prenotazioni

    # funzione di salvataggio delle modifiche apportate alla lista
    def save_data(self):
        with open('listaprenotazioni/data/lista_prenotazioni_salvata.pickle', 'wb') as handle:
            pickle.dump(self.lista_prenotazioni, handle, pickle.HIGHEST_PROTOCOL)

    # funzione che disdice una prenotazione rendendo il campo libero assegnandogli lo stato TRUE
    def disdici_by_id(self, id):
        for prenotazione in self.lista_prenotazioni:
            if prenotazione.id == id:
                prenotazione.campo.stato = True
                return True
        return False