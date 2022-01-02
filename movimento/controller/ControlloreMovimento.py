class ControlloreMovimento():
    def __init__(self, movimento):
        # il model viene assegnato al movimento selezionato
        self.model = movimento

    #richiamo le funzioni del model
    def get_id_movimento(self):
        return self.model.id

    def get_data_movimento(self):
        return self.model.data

    def get_causale_movimento(self):
        return self.model.causale

    def get_descrizione_movimento(self):
        return self.model.descrizione

    def get_importo_movimento(self):
        return self.model.importo