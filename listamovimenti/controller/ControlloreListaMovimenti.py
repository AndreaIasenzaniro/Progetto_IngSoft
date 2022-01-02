from listamovimenti.model.ListaMovimenti import ListaMovimenti


class ControlloreListaMovimenti():
    def __init__(self):
        # assegno il la lista come model al controllore della lista
        self.model = ListaMovimenti()

        # richiamo le funzioni del model

    def aggiungi_movimento(self, movimento):
        self.model.aggiungi_movimento(movimento)

    def rimuovi_movimento(self, movimento):
        self.model.rimuovi_movimento(movimento)

    def oridna_movimenti(self, lista):
        self.model.movimento_ordinato(lista)

    def get_lista_movimenti(self):
        return self.model.get_lista_movimenti()

    def get_movimento_by_index(self, index):
        return self.model.get_movimento_by_index(index)

    def elimina_movimento_by_id(self, id):
        self.model.elimina_movimento_by_id(id)

    def get_saldo(self):
        return self.model.saldo

    def save_data(self):
        self.model.save_data()