class Dipendente():

    def __init__(self, nome, cognome, datanascita, luogonascita, cf, telefono, email, abilitazione, password):
        super(Dipendente, self).__init__()
        self.id = (cognome.lower())
        self.nome = nome
        self.cognome = cognome
        self.datanascita = datanascita
        self.luogonascita = luogonascita
        self.cf = cf
        self.telefono = telefono
        self.email = email
        self.abilitazione = abilitazione
        self.password = password