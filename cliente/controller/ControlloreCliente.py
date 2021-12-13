class ControlloreCliente():
    def __init__(self, cliente):
        self.model = cliente

    def get_id_cliente(self):
        return self.model.id

    def get_nome_cliente(self):
        return self.model.nome

    def get_cognome_cliente(self):
        return self.model.cognome

    def get_cf_cliente(self):
        return self.model.cf

    def get_indirizzo_cliente(self):
        return self.model.indirizzo

    def get_email_cliente(self):
        return self.model.email

    def get_telefono_cliente(self):
        return self.model.telefono

    def get_data_nascita_cliente(self):
        return self.model.data_nascita

    def get_luogo_nascita_cliente(self):
        return self.model.luogo_nascita

    def get_residenza_cliente(self):
        return self.model.residenza

    # richiama aggiunta abbonamento model cliente
    def aggiungi_abbonamento_cliente(self, abbonamento):
        self.model.aggiungi_abbonamento(abbonamento)
    # richiama get_abbonamento model cliente
    def get_abbonamento_cliente(self):
        return self.model.get_abbonamento()
    # richiama aggiungi_certificato model cliente
    def aggiungi_certificato_cliente(self, cliente):
        self.model.aggiungi_certificato(cliente)
    # richiama get_certificato model cliente
    def get_certificato_cliente(self):
        return self.model.get_certificato()
    # controlla abbonamento e certificato di un cliente, se abbonato e senza certificati, allora indica l'abbonamento sospeso
    def get_stato_cliente(self):
        if self.get_abbonamento_cliente() == None:
            return "Cliente non abbonato"
        if self.get_certificato_cliente() == None:
            return "Sospeso, certificato mancante"
        return "Regolare"