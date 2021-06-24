from listaclienti.model.ListaClienti import ListaClienti


class ControlloreListaClienti():
    def __init__(self):
        super(ControlloreListaClienti, self).__init__()
        self.model = ListaClienti()

    def aggiungiCliente(self, cliente):
        self.model.aggiungiCliente(cliente)

    def cliente_ordinato(self, lista):
        self.model.cliente_ordinato(lista)

    def rimuovi_dalla_lista(self, cliente):
        self.model.rimuovi_dalla_lista(cliente)

    def get_lista_dei_clienti(self):
        return self.model.getListaClienti()

    def get_cliente_by_index(self, index):
        return self.model.get_cliente_by_index(index)

    def elimina_cliente_by_id(self, id):
        self.model.rimuovi_cliente_by_id(id)

    def saveData(self):
        self.model.saveData()