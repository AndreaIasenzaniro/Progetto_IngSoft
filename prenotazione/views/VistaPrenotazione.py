from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QPushButton, QHBoxLayout

from listamovimenti.controller.ControlloreListaMovimenti import ControlloreListaMovimenti
from movimento.model.Movimento import Movimento
from prenotazione.controller.ControllorePrenotazione import ControllorePrenotazione


class VistaPrenotazione(QWidget):
    def __init__(self, prenotazione, disdici_prenotazione, elimina_callback, parent = None):
        super(VistaPrenotazione, self).__init__(parent)
        self.controller = ControllorePrenotazione(prenotazione)
        self.disdici_prenotazione = disdici_prenotazione
        self.elimina_callback = elimina_callback
        self.controlloreMov = ControlloreListaMovimenti()

        v_layout = QVBoxLayout()

        v_layout.addWidget(self.crea_label("Data", self.controller.get_data_prenotazione()))
        v_layout.addWidget(self.crea_label("Ora di inizio", self.controller.get_ora_inizio()))
        v_layout.addWidget(self.crea_label("Ora di fine", self.controller.get_ora_fine()))
        v_layout.addWidget(self.crea_label("Id prenotazione", self.controller.get_id_prenotazione()))
        v_layout.addWidget(self.crea_label("Nome", self.controller.get_nome()))
        v_layout.addWidget(self.crea_label("Cognome", self.controller.get_cognome()))
        v_layout.addWidget(self.crea_label("Documento", self.controller.get_documento()))
        v_layout.addWidget(self.crea_label("Tipo campo", self.controller.get_campo_tipo()))
        v_layout.addWidget(self.crea_label("Numero campo", self.controller.get_campo_num()))

        v_layout.addItem(QSpacerItem(50, 10, QSizePolicy.Minimum, QSizePolicy.Expanding))

        btn_disdici = QPushButton("Disdici")
        btn_disdici.clicked.connect(self.disdici_prenotazione_click)
        v_layout.addWidget(btn_disdici)

        btn_esci = QPushButton("Esci")
        btn_esci.clicked.connect(self.close)
        v_layout.addWidget(btn_esci)

        self.setLayout(v_layout)

        self.setWindowTitle("Prenotazione")

    def crea_label(self, nome, funzione):
        current_label = QLabel("{}: {}".format(nome, funzione))
        current_font = current_label.font()
        current_font.setPointSize(12)
        current_label.setFont(current_font)
        return current_label

    def disdici_prenotazione_click(self):
        self.aggiungi_uscita_cassa()
        self.disdici_prenotazione(self.controller.get_id_prenotazione())
        self.elimina_callback()
        self.close()

    def aggiungi_uscita_cassa(self):
        self.movimento = Movimento(self.controller.get_data_prenotazione(), "Disdetta campo da " + str(self.controller.get_campo_tipo()) + " - ID prenotazione: " + str(self.controller.get_id_prenotazione()),"Spesa",self.controller.prezzi_campi())
        print("Stiamo aggiungendo perdita")
        self.controlloreMov.aggiungi_movimento(self.movimento)
        print("Abbiamo aggiunto perdita")
        self.controlloreMov.save_data()
        print("Abbiamo salvato perdita")