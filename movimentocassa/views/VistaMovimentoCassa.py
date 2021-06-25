from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from movimentocassa.controller.ControlloreMovimentoCassa import ControlloreMovimentoCassa


class VistaMovimentoCassa(QWidget):
    def __init__(self, movimento, elimina_movimento, elimina_callback):

        self.controller = ControlloreMovimentoCassa(movimento)
        self.elimina_movimento = elimina_movimento
        self.elimina_callback = elimina_callback

        self.v_layout = QVBoxLayout()

        self.v_layout.addWidget(QLabel("Operazione del {}".format(self.controller.get_data_movimento())))
        self.v_layout.addWidget(QLabel("Causale movimento {}".format(self.controller.get_descrizione_movimento())))
        self.v_layout.addWidget(QLabel("Importo moviemento {}".format(self.controller.get_importo_movimento())))

        self.setLayout(self.v_layout)