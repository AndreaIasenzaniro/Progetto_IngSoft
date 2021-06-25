from listamovimenticassa.controller.ControlloreListaMovimentiCassa import ControlloreListaMovimentiCassa


class MovimentoCassa():
    def __init__(self, data, descrizione, importo):
        self.controller = ControlloreListaMovimentiCassa()
        self.index = self.get_id()
        self.index += 1
        self.id = self.index
        self.data = data
        self.descrizione = descrizione
        self.importo = importo

    def get_id(self):
        if not self.controller.get_lista_movimenti():
            return 0
        else:
            indice = len(self.controller.get_lista_movimenti())-1
            movimento = self.controller.get_movimento_by_index(indice)
            id = movimento.id
            return id