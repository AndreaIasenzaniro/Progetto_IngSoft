from datetime import datetime

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QHBoxLayout, QRadioButton
from dateutil.relativedelta import relativedelta

from abbonamento.controller.ControlloreAbbonamento import ControlloreAbbonamento
from abbonamento.model.Abbonamento import Abbonamento
from listamovimenti.controller.ControlloreListaMovimenti import ControlloreListaMovimenti
from movimento.model.Movimento import Movimento


class VistaAbbonamento(QWidget):
    def __init__(self, abbonamento, callbackInsericiAbbonamento):
        super(VistaAbbonamento, self).__init__()

        #self.setFixedSize(350, 250)

        self.controller = ControlloreAbbonamento(abbonamento)
        self.controlloreMov = ControlloreListaMovimenti()
        self.callbackInserisciAbbonamento = callbackInsericiAbbonamento
        self.lista_tipo_abbonamento = ["Giornaliero","Mensile", "Trimestrale", "Annuale"]

        v_lay_abbonamento = QVBoxLayout()
        if self.controller.is_abbonato():
            v_lay_abbonamento.addWidget(QLabel("Abbonamento <b>"+ self.controller.get_tipo_abbonamento() + "</b> con scadenza " + self.controller.get_scadenza_abbonamento()))
            #v_lay.addLayout(v_lay_sup)
        else:
            #v_lay_sup.addWidget(QLabel("Registrare nuovo abbonamento o annullare."))
            #v_lay_sup.addItem(QSpacerItem(10, 10, QSizePolicy.Minimum, QSizePolicy.Minimum))
            h_lay_sup = QHBoxLayout()
            h_lay_sup.addWidget(QLabel("Seleziona il tipo di abbonamento"))
            h_lay_sup.addLayout(self.get_radio_button(self.lista_tipo_abbonamento))
            h_lay_inf = QHBoxLayout()
            self.data_in_abb = QLineEdit()
            self.data_in_abb.setPlaceholderText("gg/mm/aaaa")
            btn_aggiungi = QPushButton("Aggiungi")
            btn_aggiungi.setStyleSheet("background-color: #90ee90; font-size: 13px; font-weight: bold;")
            btn_aggiungi.setShortcut("Return")
            btn_aggiungi.clicked.connect(self.add_abbonamento_click)
            h_lay_inf.addWidget(QLabel("Inserire la data di inizio dell'abbonamento"))
            h_lay_inf.addWidget(self.data_in_abb)
            h_lay_inf.addWidget(btn_aggiungi)
            v_lay_abbonamento.addWidget(QLabel("<b>Cliente non abbonato</b>"))
            v_lay_abbonamento.addLayout(h_lay_sup)
            v_lay_abbonamento.addLayout(h_lay_inf)
        self.setLayout(v_lay_abbonamento)

    def get_radio_button(self, tipo_abbonamento):
        v_lay = QHBoxLayout()
        for item in tipo_abbonamento:
            self.radiobutton = QRadioButton(item)
            self.radiobutton.tipo = item
            #print(item)
            self.radiobutton.toggled.connect(self.scelta_radio)
            v_lay.addWidget(self.radiobutton)
        return v_lay

    def scelta_radio(self):
        self.giorni=0
        self.mesi=0
        radioButton = self.sender()
        if radioButton.isChecked():
            if radioButton.tipo == "Giornaliero":
                self.tipo_abb = "Giornaliero"
                self.prezzo_abb = 8
                self.giorni = 1
            if radioButton.tipo == "Mensile":
                self.tipo_abb = "Mensile"
                self.prezzo_abb = 35
                self.mesi = 1
            if radioButton.tipo == "Trimestrale":
                self.tipo_abb = "Trimestrale"
                self.prezzo_abb = 90
                self.mesi = 3
            if radioButton.tipo == "Annuale":
                self.tipo_abb = "Annuale"
                self.prezzo_abb = 360
                self.mesi = 12

    def add_abbonamento_click(self):
        #try:
            date = datetime.strptime(self.data_in_abb.text(), '%d/%m/%Y')
            dateUnix = datetime.timestamp(date)
            oggi = datetime.today()
            oggiUnix = datetime.timestamp(oggi)

            if oggiUnix-dateUnix<86400 :
                date += relativedelta(days=self.giorni)
                date += relativedelta(months=self.mesi)
                self.callbackInserisciAbbonamento(Abbonamento(int(date.timestamp()), self.tipo_abb, self.prezzo_abb))
                self.aggiungi_movimento()
                self.data_in_abb.setText("")
                messaggio = QMessageBox()
                messaggio.setWindowTitle("Operazione eseguita.")
                messaggio.setText("Abbonamento aggiunto correttamente.")
                messaggio.exec_()
            else:
                messaggio = QMessageBox()
                messaggio.setWindowTitle("Data errata.")
                messaggio.setText("La data inserita deve essere maggiore o uguale di quella attuale.")
                messaggio.exec_()
                self.data_in_abb.setText("")
        #except:
            #QMessageBox.critical(self, 'Errore', 'Inserisci la data nel formato richiesto: gg/mm/aaaa', QMessageBox.Ok, QMessageBox.Ok)

    def aggiungi_movimento(self):
        self.movimento = Movimento(self.data_in_abb.text(), "Sottoscrizione abbonamento {}".format(self.tipo_abb),"Incasso", float(self.prezzo_abb))
        self.movimento.isEntrata = True
        print("Stiamo aggiungendo")
        self.controlloreMov.aggiungi_movimento(self.movimento)
        print("Abbiamo aggiunto")
        self.controlloreMov.save_data()
        print("Abbiamo salvato")