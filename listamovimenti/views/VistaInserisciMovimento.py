from datetime import datetime

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox, QHBoxLayout, QLabel, QLineEdit, \
    QCalendarWidget, QRadioButton, QSpacerItem, QSizePolicy


from movimento.model.Movimento import Movimento


class VistaInserisciMovimento(QWidget):
    def __init__(self, controller, callback, parent = None):
        super(VistaInserisciMovimento, self).__init__(parent)

        self.setFixedSize(500,400)

        self.controller = controller
        self.callback = callback
        # creo un dizionario vuoto, da popolare con le voci del movimento
        self.info = {}

        self.v_layout = QVBoxLayout()

        btn_aggiungi = QPushButton("Aggiugngi")
        btn_aggiungi.setStyleSheet("background-color: #90ee90; font-size: 13px; font-weight: bold;")
        btn_aggiungi.clicked.connect(self.aggiugni_movimento)
        btn_annulla = QPushButton("Annulla")
        btn_annulla.setStyleSheet("background-color: #f08080; font-size: 13px; font-weight: bold;")
        btn_annulla.clicked.connect(self.annulla)
        btn_data = QPushButton("Inserisci data")
        btn_data.clicked.connect(self.visualizza_calendario)

        self.v_layout.addLayout(self.get_label_line("<b>Causale</b>", "Causale", "Causale"))
        self.v_layout.addLayout(self.get_label_line("<b>Importo<b/>", "Importo", "0000.00"))
        self.v_layout.addLayout(self.get_radio_button(['Incasso', 'Spesa']))
        self.v_layout.addWidget(btn_data)
        self.v_layout.addItem(QSpacerItem(45, 45, QSizePolicy.Minimum, QSizePolicy.Minimum))
        self.v_layout.addWidget(btn_aggiungi)
        self.v_layout.addWidget(btn_annulla)

        self.setLayout(self.v_layout)

    # funzione di scelta del tipo di movimento
    def get_radio_button(self, lista):
        h_lay = QHBoxLayout()
        h_lay.addWidget(QLabel("<b>Tipo di movimento<b/>"))
        # passo una lista (incasso, spesa)
        for item in lista:
            self.radiobutton = QRadioButton(item)
            self.radiobutton.tipo = item
            self.radiobutton.toggled.connect(self.scelta_radio)
            h_lay.addWidget(self.radiobutton)
        return h_lay

    # funzione che ritorna true o false a seconda della selezione del radioButton
    def scelta_radio(self):
        self.radioButton = self.sender()
        # la scelta viene usata per il calcolo del saldo totale dei movimenti
        if self.radioButton.isChecked():
            if self.radioButton.tipo == "Incasso":
                self.tipo = True
            if self.radioButton.tipo == "Spesa":
                self.tipo = False

    # funzione di visualizzazione del calendario che permette di selezionare la data
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

    # funzione che ritorna la data che viene selezionata nel calendario
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

    #funzione che ritorna un layout con una lable ed una casella di testo poste in orizzontale
    def get_label_line(self, label, tipo, placeholder):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(label))
        current_text_edit = QLineEdit(self)
        current_text_edit.setPlaceholderText(placeholder)
        layout.addWidget(current_text_edit)
        self.info[tipo] = current_text_edit
        return layout

    # funzione di annullamento di inserimento del movimento
    def annulla(self):
        self.close()
        from listamovimenti.views.VistaListaMovimenti import VistaListaMovimenti
        self.vistaListaMovimenti=VistaListaMovimenti()
        return self.vistaListaMovimenti.show()

    # funzione di aggiunta del movimento con i campi immessi nella vista di inserimento
    def aggiugni_movimento(self):
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
                print("Creo movimento")
                self.movimento = Movimento(data, causale, descrizione, importo)
                self.movimento.isEntrata = self.tipo
                self.controller.aggiungi_movimento(self.movimento)
                print("Aggiunto alla lista")
                self.controller.save_data()
                self.callback()
                self.close()
                from listamovimenti.views.VistaListaMovimenti import VistaListaMovimenti
                VistaListaMovimenti().update()
                self.vistaListaMovimenti=VistaListaMovimenti()
                return self.vistaListaMovimenti.show()
        except:
            QMessageBox.critical(self, 'Errore',
                                 'Per favore, inserisci tutte le informazioni richieste nel modo corretto',
                                 QMessageBox.Ok, QMessageBox.Ok)