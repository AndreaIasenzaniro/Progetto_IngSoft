import os
import pickle


class ListaClienti():
    def __init__(self):
        super(ListaClienti, self).__init__()
        # definisco una lista dei clienti e la popolo con i dati del file
        self.lista_clienti = []
        if os.path.isfile('listaclienti/data/lista_clienti_salvata.pickle'):
            with open('listaclienti/data/lista_clienti_salvata.pickle', 'rb') as f:
                self.lista_clienti = pickle.load(f)

    def aggiungi_cliente(self, cliente):
        self.lista_clienti.append(cliente)

    # funzione che ordina i clienti per cognome
    def cliente_ordinato(self, lista):
        lista.sort(key=lambda x: x.cognome, reverse=False)

    # funzione che rimuove il cliente dato il suo id
    def rimuovi_cliente_by_id(self, id):
        def is_selected_cliente(cliente):
            if cliente.id == id:
                return True
            return False
        self.lista_clienti.remove(list(filter(is_selected_cliente, self.lista_clienti))[0])

    def rimuovi_dalla_lista(self, cliente):
        self.lista_clienti.remove(cliente)

    #funzione che ritorna la posizione del cliente selezionato
    def get_cliente_by_index(self, index):
        return self.lista_clienti[index]

    def get_lista_clienti(self):
        return self.lista_clienti
    # funzione di salvataggio delle modifiche apportate alla lista
    def save_data(self):
        with open('listaclienti/data/lista_clienti_salvata.pickle', 'wb') as handle:
            pickle.dump(self.lista_clienti, handle, pickle.HIGHEST_PROTOCOL)