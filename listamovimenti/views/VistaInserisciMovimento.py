from datetime import datetime

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox, QHBoxLayout, QLabel, QLineEdit, \
    QCalendarWidget

from listamovimenti.controller.ControlloreListaMovimenti import ControlloreListaMovimenti
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

        btn_data = QPushButton("Inserisci data")
        btn_data.clicked.connect(self.visualizza_calendario)
        self.v_layout.addWidget(btn_data)
        self.v_layout.addLayout(self.get_label_line("Descrizione", "Descrizione", "descrzione"))
        self.v_layout.addLayout(self.get_label_line("Importo", "Importo", "importo"))

        self.v_layout.addWidget(btn_ok)
        self.v_layout.addWidget(btn_annulla)

        self.setLayout(self.v_layout)

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
        print("Oggi: " + str(oggi_unix))
        try:
            data_selezionata = self.calendario.selectedDate()
            data = "{}/{}/{}".format(data_selezionata.day(), data_selezionata.month(), data_selezionata.year())
            data_selezionata_formattata = datetime.strptime(data, '%d/%m/%Y')
            data_timestamp = datetime.timestamp(data_selezionata_formattata)

            #if oggi_unix <= data_timestamp and data_selezionata.dayOfWeek() != 7:
            self.calendario.close()
            return data
            #else:
                #return None
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, inserisci la data',QMessageBox.Ok, QMessageBox.Ok)

    def get_label_line(self, label, tipo, placeholder):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(label))
        current_text_edit = QLineEdit(self)
        current_text_edit.setPlaceholderText(placeholder)
        layout.addWidget(current_text_edit)
        self.info[tipo] = current_text_edit
        return layout

    def aggiugni_movimento(self):
        descrizione = self.info["Descrizione"].text()
        importo = self.info["Importo"].text()
        data = self.data_selezionata()
        if descrizione == "" or importo == "":
            QMessageBox.critical(self, 'Errore', 'Per favore, inserisci tutte le informazioni richieste',
                                 QMessageBox.Ok, QMessageBox.Ok)
        else:
            self.controller.aggiungi_movimento(Movimento(data, descrizione, importo))

            self.controller.save_data()
            self.callback()
            #self.close()