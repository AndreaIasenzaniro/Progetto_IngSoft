from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox, QHBoxLayout, QLabel, QLineEdit

from movimento.model.Movimento import Movimento


class VistaInserisciMovimento(QWidget):
    def __init__(self, controller, callback, parent = None):
        super(VistaInserisciMovimento, self).__init__(parent)
        self.controller = controller
        self.callback = callback
        self.info = {}

        self.v_layout = QVBoxLayout()

        btn_ok = QPushButton("Ok")
        btn_ok.clicked.connect(self.aggiugni_movimento)
        btn_annulla = QPushButton("Annulla")
        btn_annulla.clicked.connect(self.close)

        self.v_layout.addLayout(self.get_label_line("Data","Data","gg/mm/aaa"))
        self.v_layout.addLayout(self.get_label_line("Descrizione", "Descrizione", "descrzione"))
        self.v_layout.addLayout(self.get_label_line("Importo", "Importo", "importo"))

        self.v_layout.addWidget(btn_ok)
        self.v_layout.addWidget(btn_annulla)

        self.setLayout(self.v_layout)

    def get_label_line(self, label, tipo, placeholder):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(label))
        current_text_edit = QLineEdit(self)
        current_text_edit.setPlaceholderText(placeholder)
        layout.addWidget(current_text_edit)
        self.info[tipo] = current_text_edit
        return layout

    def aggiugni_movimento(self):
        data = self.info["Data"].text()
        descrizione = self.info["Descrizione"].text()
        importo = self.info["Importo"].text()

        from listamovimenti.controller.ControlloreListaMovimenti import ControlloreListaMovimenti
        controller = ControlloreListaMovimenti()
        lista = controller.get_lista_movimenti()
        if not lista:
            indice = 0
        else:
            indice = len(lista)

        if data == "" or descrizione == "" or importo == "":
            QMessageBox.critical(self, 'Errore', 'Per favore, inserisci tutte le informazioni richieste',
                                 QMessageBox.Ok, QMessageBox.Ok)
        else:
            self.controller.aggiungi_movimento(Movimento(indice, data, descrizione, importo))
            print(indice)
            self.callback()
            self.close()