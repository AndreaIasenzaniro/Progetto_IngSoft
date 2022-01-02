import os
import pickle


class ListaMovimenti():
    def __init__(self):

        # definisco una lista vuota per i movimenti
        self.lista_movimenti = []
        # se presente il file che contiene i dati della lista, lo apro e la popolo
        if os.path.isfile('listamovimenti/data/lista_movimenti_salvata.pickle'):
            with open('listamovimenti/data/lista_movimenti_salvata.pickle', 'rb') as f:
                self.lista_movimenti = pickle.load(f)

        # calcolo il saldo totale dei movimenti presenti nella lista
        self.saldo = float(0)
        for movimento in self.lista_movimenti:
            if movimento.isEntrata:
                self.saldo += float(movimento.importo)
            else:
                self.saldo -= float(movimento.importo)

    #funzione che aggiunge un movimento alla lista
    def aggiungi_movimento(self, movimento):
        self.lista_movimenti.append(movimento)

    # funzione che rimuove un movimentto dalla lista
    def rimuovi_movimento(self, movimento):
        self.lista_movimenti.remove(movimento)

    # funzione che elimina un movimento dalla lista prendendo il suo id
    def elimina_movimento_by_id(self, id):
        def is_selected_movimento(movimento):
            if movimento.id == id:
                return True
            return False
        self.lista_movimenti.remove(list(filter(is_selected_movimento, self.lista_movimenti))[0])

    # funzione che ordina i movimento per data crescente
    def movimento_ordinato(self, lista):
        lista.sort(key=lambda x: x.data, reverse=False)

    #funzione che ritorna il movimento all'indice della lista passato
    def get_movimento_by_index(self, index):
        return self.lista_movimenti[index]

    def get_lista_movimenti(self):
        return self.lista_movimenti

    def save_data(self):
        with open('listamovimenti/data/lista_movimenti_salvata.pickle', 'wb') as handle:
            pickle.dump(self.lista_movimenti, handle, pickle.HIGHEST_PROTOCOL)

