from listamovimenti.controller.ControlloreListaMovimenti import ControlloreListaMovimenti


class Movimento():
    def __init__(self, data, causale, descrizione, importo):

        self.controller = ControlloreListaMovimenti()
        if not self.controller.get_lista_movimenti():
            self.id = 0
        else:
            index = len(self.controller.get_lista_movimenti())
            self.id = index + 1

        self.data = data
        self.causale = causale
        self.importo = importo
        self.descrizione = descrizione
        self.isEntrata = False