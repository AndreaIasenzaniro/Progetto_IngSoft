from listaclienti.model.ListaClienti import ListaClienti


class ControlloreListaClienti():
    def __init__(self):
        super(ControlloreListaClienti, self).__init__()
        self.model = ListaClienti()

    # richiamo funzioni del model

    def aggiungi_cliente(self, cliente):
        self.model.aggiungi_cliente(cliente)

    def cliente_ordinato(self, lista):
        self.model.cliente_ordinato(lista)

    def rimuovi_dalla_lista(self, cliente):
        self.model.rimuovi_dalla_lista(cliente)

    def get_lista_dei_clienti(self):
        return self.model.get_lista_clienti()

    def get_cliente_by_index(self, index):
        return self.model.get_cliente_by_index(index)

    def elimina_cliente_by_id(self, id):
        self.model.rimuovi_cliente_by_id(id)

    def save_data(self):
        self.model.save_data()