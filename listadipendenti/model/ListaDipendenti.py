import os
import pickle


class ListaDipendenti():
    def __init__(self):
        super(ListaDipendenti, self).__init__()
        # definisco una lista vuota per i dipendenti
        self.lista_dipendenti = []
        # se presente il file che contiene i dati della lista, lo apro e la popolo
        if os.path.isfile('listadipendenti/data/lista_dipendenti_salvata.pickle'):
            with open('listadipendenti/data/lista_dipendenti_salvata.pickle', 'rb') as f:
                self.lista_dipendenti = pickle.load(f)

    # funzione che aggiugne un dipendente alla lista
    def aggiungi_dipendente(self, dipendente):
        self.lista_dipendenti.append(dipendente)

    # funzione che ordina i dipendenti per cognome
    def ordina_dipendenti(self, lista):
        lista.sort(key=lambda x:x.cognome, reverse = False)

    # funzione che rimuove un dipendente , dato il suo id
    def rimuovi_dipendente_by_id(self, id):
        def is_selected_dipendente(dipendente):
            if dipendente.id == id:
                return True
            return False
        self.lista_dipendenti.remove(list(filter(is_selected_dipendente, self.lista_dipendenti))[0])

    def rimuovi_dalla_lista(self, dipendente):
        self.lista_dipendenti.remove(dipendente)

    # funzione che ritorna la posizione del dipendente selezionato nella lsita
    def get_dipendente_by_index(self, index):
        return self.lista_dipendenti[index]

    # funzione che ritorna la lista dei dipendenti
    def get_lista_dipendenti(self):
        return self.lista_dipendenti

    # funzione di salvataggio delle modifiche apportate alla lista
    def save_data(self):
        with open('listadipendenti/data/lista_dipendenti_salvata.pickle', 'wb') as handle:
            pickle.dump(self.lista_dipendenti, handle, pickle.HIGHEST_PROTOCOL)