from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton

from movimento.controller.ControlloreMovimento import ControlloreMovimento


class VistaMovimento(QWidget):
    def __init__(self, movimento, elimina_movimento, elimina_callback, parent = None):
        super(VistaMovimento, self).__init__(parent)

        self.controller = ControlloreMovimento(movimento)
        self.elimina_movimento = elimina_movimento
        self.elimina_callback = elimina_callback

        self.v_layout = QVBoxLayout()

        btn_chiudi = QPushButton("Chiudi")
        btn_chiudi.clicked.connect(self.close)
        btn_elimina = QPushButton("Elimina")
        btn_elimina.clicked.connect(self.elimina_movimento_click)

        self.v_layout.addWidget(QLabel("Operazione del {}".format(self.controller.get_data_movimento())))
        self.v_layout.addWidget(QLabel("Causale movimento {}".format(self.controller.get_causale_movimento())))
        self.v_layout.addWidget(QLabel("Importo moviemento {}".format(self.controller.get_importo_movimento())))

        self.setLayout(self.v_layout)

    def elimina_movimento_click(self):
        self.elimina_movimento(self.controller.get_id_movimento())
        self.elimina_callback()
        self.close()