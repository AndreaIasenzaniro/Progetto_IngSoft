class ControlloreDipendente():

    def __init__(self, dipendente):
        # il model è del dipendente che vine passato
        self.model = dipendente

    def get_id_dipendente(self):
        return self.model.id

    def get_nome_dipendente(self):
        return self.model.nome

    def get_cognome_dipendente(self):
        return self.model.cognome

    def get_data_dipendente(self):
        return self.model.data_nascita

    def get_luogo_dipendente(self):
        return self.model.luogo_nascita

    def get_residenza_dipendente(self):
        return self.model.residenza

    def get_indirizzo_dipendente(self):
        return self.model.indirizzo

    def get_cf_dipendente(self):
        return self.model.cf

    def get_telefono_dipendente(self):
        return self.model.telefono

    def get_email_dipendente(self):
        return self.model.email

    def get_abilitazione_dipendente(self):
        return self.model.abilitazione

    def get_password_dipendente(self):
        return self.model.password
