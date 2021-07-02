import os
import pickle


class ListaMovimenti():
    def __init__(self):

        self.lista_movimenti = []
        if os.path.isfile('listamovimenti/data/lista_movimenti_salvata.pickle'):
            with open('listamovimenti/data/lista_movimenti_salvata.pickle', 'rb') as f:
                self.lista_movimenti = pickle.load(f)

        self.get_saldo_cassa()

    def aggiungi_movimento(self, movimento):
        self.lista_movimenti.append(movimento)

    def rimuovi_movimento(self, prenotazione):
        self.lista_movimenti.remove(prenotazione)

    def elimina_movimento_by_id(self, id):
        def is_selected_movimento(movimento):
            if movimento.id == id:
                return True
            return False
        self.lista_movimenti.remove(list(filter(is_selected_movimento, self.lista_movimenti))[0])

    def movimento_ordinato(self, lista):
        lista.sort(key=lambda x: x.data, reverse=False)

    def get_movimento_by_index(self, index):
        return self.lista_movimenti[index]

    def get_lista_movimenti(self):
        return self.lista_movimenti

    def get_saldo_cassa(self):
        saldo = 0
        for movimento in self.lista_movimenti:
            if movimento.isEntrata:
                saldo += float(movimento.importo)
            else:
                saldo -= float(movimento.importo)
        return round(saldo, 2)

    def save_data(self):
        with open('listamovimenti/data/lista_movimenti_salvata.pickle', 'wb') as handle:
            pickle.dump(self.lista_movimenti, handle, pickle.HIGHEST_PROTOCOL)

