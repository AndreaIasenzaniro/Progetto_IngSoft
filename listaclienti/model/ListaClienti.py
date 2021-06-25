import os
import pickle


class ListaClienti():
    def __init__(self):
        super(ListaClienti, self).__init__()
        self.lista_clienti = []
        if os.path.isfile('listaclienti/data/lista_clienti_salvata.pickle'):
            with open('listaclienti/data/lista_clienti_salvata.pickle', 'rb') as f:
                self.lista_clienti = pickle.load(f)

    def aggiungiCliente(self, cliente):
        self.lista_clienti.append(cliente)

    def cliente_ordinato(self, lista):
        lista.sort(key=lambda x: x.cognome, reverse=False)

    def rimuovi_cliente_by_id(self, id):
        def is_selected_cliente(cliente):
            if cliente.id == id:
                return True
            return False
        self.lista_clienti.remove(list(filter(is_selected_cliente, self.lista_clienti))[0])

    def rimuovi_dalla_lista(self, cliente):
        self.lista_clienti.remove(cliente)

    def get_cliente_by_index(self, index):
        return self.lista_clienti[index]

    def getListaClienti(self):
        return self.lista_clienti

    def saveData(self):
        with open('listaclienti/data/lista_clienti_salvata.pickle', 'wb') as handle:
            pickle.dump(self.lista_clienti, handle, pickle.HIGHEST_PROTOCOL)