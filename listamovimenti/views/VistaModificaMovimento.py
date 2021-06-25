from movimento.controller.ControlloreMovimento import ControlloreMovimento


class VistaModificaMovimentoCassa():
    def __init__(self, movimento_selezionato, controller, callback):
        self.mov_sel = movimento_selezionato
        self.movimento = ControlloreMovimento(movimento_selezionato)
        self.controller = controller
        self.callback = callback
        self.info = {}