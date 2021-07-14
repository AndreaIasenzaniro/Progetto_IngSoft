from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit

from movimento.controller.ControlloreMovimento import ControlloreMovimento


class VistaModificaMovimentoCassa():
    def __init__(self, movimento_selezionato, controller, callback):
        self.mov_sel = movimento_selezionato
        self.movimento = ControlloreMovimento(movimento_selezionato)
        self.controller = controller
        self.callback = callback
        self.info = {}

        btn_modifica = QPushButton("Modifica")
        btn_modifica.clicked.connect(self.mod_movimento)

        btn_annulla = QPushButton("Annulla")
        btn_annulla.clicked.connect(self.close)

        self.v_layout = QVBoxLayout()

        self.v_layout.addLayout(self.get_label_line("Causale", self.movimento.get_causale_movimento(),"Causale"))
        self.v_layout.addLayout(self.get_label_line("Importo", self.movimento.get_importo_movimento(), "Importo"))
        self.v_layout.addLayout(self.get_label_line("Data", self.movimento.get_data_movimento()))

    def get_label_line(self, tipo, campo, testo):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(testo))
        current_text_edit = QLineEdit(self)
        current_text_edit.setText(campo)
        layout.addWidget(current_text_edit)
        self.info[tipo] = current_text_edit
        return layout

