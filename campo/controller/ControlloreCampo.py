class ControlloreCampo():
    def __init__(self, campo):
        self.model=campo

    def get_tipo(self):
        return self.model.tipo_abb_selezionato

    def get_numero(self):
        return self.model.numero

    def get_campo_disponibile(self):
        if(self.model.is_disponibile()):
            return "Disponibile"
        else:
            return "Non disponibile"