class Cliente():
    def __init__(self, id, nome, cognome, cf, data_nascita, luogo_nascita, residenza,  indirizzo, email, telefono):
        super(Cliente, self).__init__()
        self.id = id
        self.nome = nome
        self.cognome = cognome
        self.cf = cf
        self.indirizzo = indirizzo
        self.email = email
        self.telefono = telefono
        self.data_nascita = data_nascita
        self.luogo_nascita = luogo_nascita
        self.residenza = residenza
        self.abbonamento = None
        self.certificato = None

    def aggiungi_abbonamento(self, abbonamento):
        self.abbonamento = abbonamento

    def get_abbonamento(self):
        if self.abbonamento is None:
            return None
        elif self.abbonamento.abb_in_corso():
                return self.abbonamento

    def aggiungi_certificato(self, certificato):
        self.certificato = certificato

    def get_certificato(self):
        if self.certificato is None:
            return None
        elif self.certificato.inCorso():
            return self.certificato