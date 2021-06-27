from datetime import datetime

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox,QHBoxLayout

from certificato.controller.ControlloreCertificato import ControlloreCertificato
from certificato.model.Certificato import Certificato


class VistaCertificato(QWidget):
    def __init__(self, certificato, callbackInsericiCertificato):
        super(VistaCertificato, self).__init__()
        self.controller = ControlloreCertificato(certificato)
        self.callbackInsericiCertificato = callbackInsericiCertificato

        h_lay_certificato = QHBoxLayout()
        if self.controller.isValido():
            h_lay_certificato.addWidget(QLabel("Il certificato medico scade in data: " + self.controller.getScadenza()))
        else:
            h_lay_certificato.addWidget(QLabel("Inserire la data di scadenza del certificato."))
            self.scadenza = QLineEdit()
            self.scadenza.setPlaceholderText("gg/mm/aaaa")
            h_lay_certificato.addWidget(self.scadenza)
            orizLayout = QHBoxLayout()
            inserisci = QPushButton("Aggiungi")
            inserisci.clicked.connect(self.aggiungi_certificato_click)
            orizLayout.addWidget(inserisci)
            '''annulla = QPushButton("Annulla")
            annulla.clicked.connect(self.close)
            orizLayout.addWidget(annulla)'''
            h_lay_certificato.addLayout(orizLayout)

        self.setLayout(h_lay_certificato)

    def aggiungi_certificato_click(self):
        try:
            date = datetime.strptime(self.scadenza.text(), '%d/%m/%Y')
            dateUnix = datetime.timestamp(date)
            oggi = datetime.today()
            oggiUnix = datetime.timestamp(oggi)

            if dateUnix >= oggiUnix:
                self.callbackInsericiCertificato(Certificato(date.timestamp()))
                self.scadenza.setText("")
                messaggio = QMessageBox()
                messaggio.setWindowTitle("Operazione eseguita.")
                messaggio.setText("Certificato aggiunto correttamente.")
                messaggio.exec_()
            else:
                messaggio = QMessageBox()
                messaggio.setWindowTitle("Data errata.")
                messaggio.setText("Inserisci una data valida, maggiore di quella aattuale.")
                messaggio.exec_()
                self.scadenza.setText("")
        except:
            QMessageBox.critical(self, 'Errore', 'Inserisci la data nel formato richiesto: gg/mm/aaaa', QMessageBox.Ok, QMessageBox.Ok)