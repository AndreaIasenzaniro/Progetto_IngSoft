from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QCalendarWidget, QLabel, QListView, QPushButton
from PyQt5.QtCore import Qt

from listaprenotazioni.controller.ControlloreListaPrenotazioni import ControlloreListaPrenotazioni
from listaprenotazioni.views.VistaInserisciPrenotazione import VistaInserisciPrenotazione
from listaprenotazioni.views.VistaListaPrenotazioni import VistaListaPrenotazioni

class Calendario(QWidget):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setFixedSize(750, 450)
        self.Calendar()
        self.controller = ControlloreListaPrenotazioni()
        self.list_view = QListView()
        self.update_ui()
        self.setLayout(self.vbox)
        self.show()

    def Calendar(self):
        self.vbox = QVBoxLayout()
        self.calendario = QCalendarWidget()
        self.calendario.setGridVisible(True)
        self.calendario.clicked.connect(self.data_selezionata)
        self.vbox.addWidget(self.calendario)

        new_button = QPushButton("Aggiungi prenotazione")
        new_button.clicked.connect(self.show_new_prenotazione)
        self.vbox.addWidget(new_button)

        btn_esc = QPushButton("Esci")
        btn_esc.clicked.connect(self.funz_esci)
        self.vbox.addWidget(btn_esc)

    def data_selezionata(self):
        data_selezionata = self.calendario.selectedDate()
        data_da_usare = "{}/{}/{}".format(data_selezionata.day(), data_selezionata.month(), data_selezionata.year())
        self.vista_lista_prenotazioni = VistaListaPrenotazioni(data_da_usare)
        self.vista_lista_prenotazioni.show()

    def show_new_prenotazione(self):
        self.vista_inserisci_prenotazione = VistaInserisciPrenotazione(self.controller, self.update_ui)
        self.vista_inserisci_prenotazione.show()

    def update_ui(self):
        pass

    def funz_esci(self):
        from home.views.VistaHome import VistaHome
        self.vista_home = VistaHome()
        self.close()
        return self.vista_home.show()