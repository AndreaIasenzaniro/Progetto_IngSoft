from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QWidget, QRadioButton, \
    QCalendarWidget, QMessageBox, QSpacerItem, QSizePolicy

from movimento.controller.ControlloreMovimento import ControlloreMovimento
from datetime import datetime

from movimento.model.Movimento import Movimento


class VistaModificaMovimento(QWidget):
    def __init__(self, movimento_selezionato, controller, callback):
        super(VistaModificaMovimento, self).__init__()

        self.setFixedSize(350, 300)
        self.mov_sel = movimento_selezionato
        self.movimento = ControlloreMovimento(movimento_selezionato)
        self.controller = controller
        self.callback = callback
        self.info = {}

        btn_modifica = QPushButton("Modifica")
        btn_modifica.setStyleSheet("background-color: #90ee90; font-size: 13px; font-weight: bold;")
        btn_modifica.setShortcut("Return")
        btn_modifica.clicked.connect(self.mod_movimento)

        btn_annulla = QPushButton("Annulla")
        btn_annulla.setStyleSheet("background-color: #f08080; font-size: 13px; font-weight: bold;")
        btn_annulla.setShortcut("Esc")
        btn_annulla.clicked.connect(self.annulla)

        btn_data = QPushButton("Inserisci data")
        btn_data.clicked.connect(self.visualizza_calendario)

        self.v_layout = QVBoxLayout()

        self.v_layout.addLayout(self.get_label_line("<b>Causale</b>", "Causale", self.movimento.get_causale_movimento()))
        self.v_layout.addLayout(self.get_label_line("<b>Importo<b/>", "Importo", self.movimento.get_importo_movimento()))
        self.v_layout.addLayout(self.get_radio_button(['Incasso', 'Spesa']))
        self.v_layout.addWidget(btn_data)
        self.v_layout.addItem(QSpacerItem(45, 45, QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.v_layout.addWidget(btn_modifica)
        self.v_layout.addWidget(btn_annulla)

        self.setLayout(self.v_layout)
        self.setWindowTitle("Modifica Movimento")

    def get_label_line(self, label, tipo, placeholder):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(label))
        current_text_edit = QLineEdit(self)
        current_text_edit.setText(placeholder)
        layout.addWidget(current_text_edit)
        self.info[tipo] = current_text_edit
        return layout


    def get_radio_button(self, lista):
        h_lay = QHBoxLayout()
        h_lay.addWidget(QLabel("<b>Tipo di movimento<b/>"))
        for item in lista:
            self.radiobutton = QRadioButton(item)
            self.radiobutton.tipo = item
            self.radiobutton.toggled.connect(self.scelta_radio)
            h_lay.addWidget(self.radiobutton)
        return h_lay

    def scelta_radio(self):
        self.radioButton = self.sender()
        if self.radioButton.isChecked():
            if self.radioButton.tipo == "Incasso":
                self.tipo = True
            if self.radioButton.tipo == "Spesa":
                self.tipo = False

    def visualizza_calendario(self):
        self.window = QWidget()
        self.v1_layout = QVBoxLayout()
        self.calendario = QCalendarWidget()
        self.calendario.setGridVisible(True)

        self.v1_layout.addWidget(self.calendario)
        self.btn_conferma = QPushButton("Conferma")
        self.btn_conferma.clicked.connect(self.window.close)
        self.v1_layout.addWidget(self.btn_conferma)

        self.window.setLayout(self.v1_layout)
        self.window.show()

    def data_selezionata(self):
        oggi = datetime.today()
        oggi_formattato = oggi.strftime("%d/%m/%Y")
        oggi_formattato_per_unix = datetime.strptime(oggi_formattato, '%d/%m/%Y')
        oggi_unix = datetime.timestamp(oggi_formattato_per_unix)
        try:
            data_selezionata = self.calendario.selectedDate()
            data = "{}/{}/{}".format(data_selezionata.day(), data_selezionata.month(), data_selezionata.year())
            self.calendario.close()
            return data
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, inserisci la data',QMessageBox.Ok, QMessageBox.Ok)

    def annulla(self):
        self.close()
        from listamovimenti.views.VistaListaMovimenti import VistaListaMovimenti
        self.vistaListaMovimenti=VistaListaMovimenti()
        return self.vistaListaMovimenti.show()

    def mod_movimento(self):
        try:
            data = self.data_selezionata()
            causale = self.info["Causale"].text()
            descrizione = str(self.radioButton.tipo)
            if isinstance(float(self.info["Importo"].text()), float):
                importo = self.info["Importo"].text()
            else:
                QMessageBox.critical(self, 'Errore', 'Per favore, inserisci un importo valido',
                                     QMessageBox.Ok, QMessageBox.Ok)
            if descrizione == "":
                QMessageBox.critical(self, 'Errore', 'Per favore, inserisci tutte le informazioni richieste',
                                     QMessageBox.Ok, QMessageBox.Ok)
            else:
                movimento = Movimento(data, causale, descrizione, importo)
                movimento.isEntrata = self.tipo
                self.controller.rimuovi_movimento(self.mov_sel)
                self.controller.aggiungi_movimento(movimento)
                self.controller.save_data()
                self.callback()
                self.close()
                from listamovimenti.views.VistaListaMovimenti import VistaListaMovimenti
                VistaListaMovimenti().update()
                self.vistaListaMovimenti = VistaListaMovimenti()
                return self.vistaListaMovimenti.show()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, inserisci tutte le informazioni richieste nel modo corretto',
                                 QMessageBox.Ok, QMessageBox.Ok)