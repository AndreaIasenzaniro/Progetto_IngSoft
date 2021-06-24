class Campo():
    def __init__(self, tipo, numero):
        self.tipo=tipo
        self.numero=numero
        self.stato = True

    def is_disponibile(self):
        return self.stato

    def prenota(self):
        self.stato=False