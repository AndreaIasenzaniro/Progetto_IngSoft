class Dipendente():

    def __init__(self, nome, cognome, data_nascita, luogo_nascita, residenza, indirizzo, cf, telefono, email, abilitazione, password):
        super(Dipendente, self).__init__()
        self.id = (cognome.lower())
        self.nome = nome
        self.cognome = cognome
        self.data_nascita = data_nascita
        self.luogo_nascita = luogo_nascita
        self.residenza = residenza
        self.indirizzo = indirizzo
        self.cf = cf
        self.telefono = telefono
        self.email = email
        self.abilitazione = abilitazione
        self.password = password