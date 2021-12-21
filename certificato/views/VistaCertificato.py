from datetime import datetime

from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QMessageBox,QHBoxLayout

from certificato.controller.ControlloreCertificato import ControlloreCertificato
from certificato.model.Certificato import Certificato


class VistaCertificato(QWidget):
    def __init__(self, certificato, callbackInsericiCertificato):
        super(VistaCertificato, self).__init__()
        self.controller = ControlloreCertificato(certificato)
        self.callbackInsericiCertificato = callbackInsericiCertificato

        h_lay_certificato = QHBoxLayout()
        #verifichiamo che il certificato sia in corso di validità
        if self.controller.isValido():
            #essendo in corso di validità mostriamo la scadenza
            h_lay_certificato.addWidget(QLabel("Il certificato medico scade in data: " + self.controller.getScadenza()))
        #se non si possiede un certificato in corso di validità lo si può aggiungere
        else:
            h_lay_certificato.addWidget(QLabel("Inserire la data di scadenza del certificato."))
            self.scadenza = QLineEdit()
            self.scadenza.setPlaceholderText("gg/mm/aaaa")
            h_lay_certificato.addWidget(self.scadenza)
            orizLayout = QHBoxLayout()
            btn_aggiungi = QPushButton("Aggiungi")
            btn_aggiungi.setStyleSheet("background-color: #90ee90; font-size: 13px; font-weight: bold;")
            #colleghiamo il pulsante invio della tastiera al pulsante aggiungi dell'interfaccia
            btn_aggiungi.setShortcut("Return")
            #colleghiamo il bottone aggiungi con la funzione che effettivamente aggiunge il certificato
            btn_aggiungi.clicked.connect(self.aggiungi_certificato_click)
            orizLayout.addWidget(btn_aggiungi)
            h_lay_certificato.addLayout(orizLayout)

        self.setLayout(h_lay_certificato)

    #funzione che aggiunge il certificato
    def aggiungi_certificato_click(self):
        try:
            #nelle seguenti due righe formattiamo in datetime la data di fine del certificato da aggiungere e otteniamo il suo timestamp
            date = datetime.strptime(self.scadenza.text(), '%d/%m/%Y')
            dateUnix = datetime.timestamp(date)
            #nelle seguenti due righe formattiamo in datetime la data di oggi il suo timestamp
            oggi = datetime.today()
            oggiUnix = datetime.timestamp(oggi)

            #se la scadenza dell'certificato avviene lo stesso giorno o un giorno seguente alla data odierna, aggiungiamo correttamente il
            #certificato
            if dateUnix >= oggiUnix:
                self.callbackInsericiCertificato(Certificato(date.timestamp()))
                self.scadenza.setText("")
                messaggio = QMessageBox()
                messaggio.setWindowTitle("Operazione eseguita.")
                messaggio.setText("Certificato aggiunto correttamente.")
                messaggio.exec_()
            #se la condizione precedente non si verifica, è stata inserita una data di scadenza del certificato già passata per cui non valida
            else:
                messaggio = QMessageBox()
                messaggio.setWindowTitle("Data errata.")
                messaggio.setText("Inserisci una data valida, maggiore di quella attuale.")
                messaggio.exec_()
                self.scadenza.setText("")
        except:
            QMessageBox.critical(self, 'Errore', 'Inserisci la data nel formato richiesto: gg/mm/aaaa', QMessageBox.Ok, QMessageBox.Ok)
            self.scadenza.setText("")