from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget, QListView, QPushButton,QHBoxLayout

from listaprenotazioni.controller.ControlloreListaPrenotazioni import ControlloreListaPrenotazioni
from listaprenotazioni.views.VistaInserisciPrenotazione import VistaInserisciPrenotazione
from listaprenotazioni.views.VistaListaPrenotazioni import VistaListaPrenotazioni

class Calendario(QWidget):
    vista_prenotazione = False
    def __init__(self, parent = None):
        super().__init__(parent)

        self.setFixedSize(1250, 700)
        self.Calendar()
        self.controller = ControlloreListaPrenotazioni()
        self.list_view = QListView()
        self.update_ui()
        self.h_layout = QHBoxLayout()

        from home.views.VistaHome import VistaHome
        self.setWindowTitle("Campo da {}".format(VistaHome().selezione_campo))
        self.h_layout.addLayout(self.vbox)
        self.setLayout(self.h_layout)
        self.show()

    #funzione che crea il calendario concretamente
    def Calendar(self):
        self.vbox = QVBoxLayout()
        self.calendario = QCalendarWidget()
        #settiamo a visibile la griglia nel calendario per facilitare la distinzione dei giorni
        self.calendario.setGridVisible(True)
        self.calendario.clicked.connect(self.data_selezionata)
        self.vbox.addWidget(self.calendario)

        new_button = QPushButton("Aggiungi prenotazione")
        new_button.clicked.connect(self.show_new_prenotazione)
        self.vbox.addWidget(new_button)

        btn_esc = QPushButton("Esci")
        btn_esc.clicked.connect(self.funz_esci)
        self.vbox.addWidget(btn_esc)

    #questa funzione acquisisce e salva la data che andiamo a selezionare (clickare) sul calendario, la formatta in un
    #formato a noi comodo e la salva in un ulteriore variabile che andremo a passare nel costruttore VistaListaPrenotazioni
    #per far vedere la lista delle prenotazioni di quel giorno
    def data_selezionata(self):
        data_selezionata = self.calendario.selectedDate()
        data_da_usare = "{}/{}/{}".format(data_selezionata.day(), data_selezionata.month(), data_selezionata.year())
        self.vista_lista_prenotazioni = VistaListaPrenotazioni(data_da_usare)
        #self.close()
        self.vista_lista_prenotazioni.show()
        #chiudo calendario quando clicco sul giorno
        #self.close()

    #questa funzione apre l'interfaccia per l'inserimento di una nuova prenotazione
    def show_new_prenotazione(self):
        self.vista_inserisci_prenotazione = VistaInserisciPrenotazione(self.controller, self.update_ui)
        #self.vista_inserisci_prenotazione.show()
        self.v_lay = QHBoxLayout()
        if Calendario.vista_prenotazione == False:
            #self.v_lay.addStretch()
            self.v_lay.addWidget(self.vista_inserisci_prenotazione)
            #self.v_lay.addStretch()
            self.h_layout.addLayout(self.v_lay)
            Calendario.vista_prenotazione = True
        elif Calendario.vista_prenotazione == True:
            pass

    def update_ui(self):
        pass

    #chiude la nostra pagina con il calendario
    def funz_esci(self):
        from home.views.VistaHome import VistaHome
        self.vista_home = VistaHome()
        self.close()
        Calendario.vista_prenotazione = False
        return self.vista_home.show()