from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListView, QVBoxLayout, QPushButton, QMessageBox, QTableWidgetItem, \
    QTableWidget, QHeaderView
from PyQt5.QtCore import Qt

from dipendente.views.VistaDipendente import VistaDipendente
from listadipendenti.controller.ControlloreListaDipendenti import ControlloreListaDipendenti
from listadipendenti.views.VistaInserisciDipendente import VistaInserisciDipendente
from listadipendenti.views.VistaModificaDipendente import  VistaModificaDipendente


class VistaListaDipendenti(QWidget):
    def __init__(self, parent=None):
        super(VistaListaDipendenti, self).__init__(parent)

        self.setFixedSize(800, 500)
        self.move(250, 100)

        self.controller = ControlloreListaDipendenti()
        #self.list_view = QListView()
        #self.update_ui()
        self.createTable()
        self.list_view = self.tableWidget

        # definisco un layout orizzontale per la pagina
        h_layout = QHBoxLayout()
        # definisco un layout verticale per i pulsanti
        btn_layout = QVBoxLayout()
        # creazione pulsante di apertura del dipendente
        btn_apri = QPushButton("Apri")
        btn_apri.setStyleSheet("background-color: ; font-size: 15px; font-weight: bold;")
        btn_apri.clicked.connect(self.show_selected_info)
        # creazione pulsante modifica del dipendente
        btn_modifica = QPushButton("Modifica")
        btn_modifica.setStyleSheet("background-color: ; font-size: 15px; font-weight: bold;")
        btn_modifica.clicked.connect(self.modifica_dipendente)
        # creazione pulsante di aggiunta di un nuovo dipendente
        btn_nuovo = QPushButton("Nuovo")
        btn_nuovo.setStyleSheet("background-color: ; font-size: 15px; font-weight: bold;")
        btn_nuovo.clicked.connect(self.show_new_dipendente)
        # creazione pulsante di chiusura della finestra
        btn_esci = QPushButton("Esci")
        btn_esci.setShortcut("Esc")
        btn_esci.clicked.connect(self.funz_indietro)

        # aggiunta pulsanti al layout dei pulsanti
        btn_layout.addWidget(btn_nuovo)
        btn_layout.addWidget(btn_modifica)
        btn_layout.addWidget(btn_apri)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_esci)

        # aggiunta visualizzazione della lista al layout
        #h_layout.addWidget(self.list_view)
        h_layout.addWidget(self.tableWidget)
        # aggiunta layout pulsanti al layout principale
        h_layout.addLayout(btn_layout)
        btn_layout.addStretch()

        # setting del layout della finestra
        self.setLayout(h_layout)
        self.setWindowTitle('Gestione Dipendenti')

    def show_selected_info(self):
        try:
            self.selected_elimina = self.list_view.selectedIndexes()[0].row()
            dipendente_selezionato = self.controller.get_dipendente_by_index(self.selected_elimina)
            self.vista_dipendente = VistaDipendente(dipendente_selezionato, self.controller.elimina_dipendente_by_id, self.update_elimina)
            self.vista_dipendente.show()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un dipendente da visualizzare.', QMessageBox.Ok, QMessageBox.Ok)

    def show_new_dipendente(self):
        self.vista_inserisci_dipendente = VistaInserisciDipendente(self.controller, self.update_new)
        self.vista_inserisci_dipendente.show()

    def modifica_dipendente(self):
        try:
            selected = self.list_view.selectedIndexes()[0].row()
            dipendente_selezionato = self.controller.get_dipendente_by_index(selected)
            self.vista_dipendente_mod = VistaModificaDipendente(dipendente_selezionato, self.controller, self.update_mod)
            self.vista_dipendente_mod.show()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un dipendente da modificare.', QMessageBox.Ok, QMessageBox.Ok)

    def funz_indietro(self):
        from home.views.VistaHome import VistaHome
        self.vista_home = VistaHome()
        self.close()
        return self.vista_home.show()

    # Create table
    def createTable(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)

        # Row count
        self.tableWidget.setRowCount(len(self.controller.get_lista_dipendenti()))
        #rows = self.controller.get_lista_dipendenti()

        # Column count
        self.tableWidget.setColumnCount(7)
        columns = ['Cognome', 'Nome', 'Codice fiscale', 'Data di nascita', 'Luogo di nascita', 'Abilitazione', 'Email']
        self.tableWidget.setHorizontalHeaderLabels(columns)
        self.controller.ordina_dipendenti(self.controller.get_lista_dipendenti())

        # inserimento dipendenti nella tableWidget
        self.i = 0
        for dipendente in self.controller.get_lista_dipendenti():
            #self.tableWidget.setItem(self.i, 0, QTableWidgetItem(dipendente.id))
            self.tableWidget.setItem(self.i, 0, QTableWidgetItem(dipendente.cognome))
            self.tableWidget.setItem(self.i, 1, QTableWidgetItem(dipendente.nome))
            self.tableWidget.setItem(self.i, 2, QTableWidgetItem(dipendente.cf))
            self.tableWidget.setItem(self.i, 3, QTableWidgetItem(dipendente.datanascita))
            self.tableWidget.setItem(self.i, 4, QTableWidgetItem(dipendente.luogonascita))
            self.tableWidget.setItem(self.i, 5, QTableWidgetItem(dipendente.abilitazione))
            self.tableWidget.setItem(self.i, 6, QTableWidgetItem(dipendente.email))
            self.i += 1

        # Table will fit the screen horizontally
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        #self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def update_elimina(self):
        riga = self.selected_elimina
        self.tableWidget.removeRow(riga)

    def update_new(self):
        #count ultimo dipendente
        c = len(self.controller.get_lista_dipendenti())
        #aggiungi una riga
        self.tableWidget.setRowCount(c)
        self.controller.ordina_dipendenti(self.controller.get_lista_dipendenti())
        # inserimento dipendente nella tableWidget
        self.i = 0
        for dipendente in self.controller.get_lista_dipendenti():
            self.tableWidget.setItem(self.i, 0, QTableWidgetItem(dipendente.cognome))
            self.tableWidget.setItem(self.i, 1, QTableWidgetItem(dipendente.nome))
            self.tableWidget.setItem(self.i, 2, QTableWidgetItem(dipendente.cf))
            self.tableWidget.setItem(self.i, 3, QTableWidgetItem(dipendente.datanascita))
            self.tableWidget.setItem(self.i, 4, QTableWidgetItem(dipendente.luogonascita))
            self.tableWidget.setItem(self.i, 5, QTableWidgetItem(dipendente.abilitazione))
            self.tableWidget.setItem(self.i, 6, QTableWidgetItem(dipendente.email))
            self.i += 1

    def update_mod(self):
        self.controller.ordina_dipendenti(self.controller.get_lista_dipendenti())
        # inserimento dipendente nella tableWidget
        self.i = 0
        for dipendente in self.controller.get_lista_dipendenti():
            self.tableWidget.setItem(self.i, 0, QTableWidgetItem(dipendente.cognome))
            self.tableWidget.setItem(self.i, 1, QTableWidgetItem(dipendente.nome))
            self.tableWidget.setItem(self.i, 2, QTableWidgetItem(dipendente.cf))
            self.tableWidget.setItem(self.i, 3, QTableWidgetItem(dipendente.datanascita))
            self.tableWidget.setItem(self.i, 4, QTableWidgetItem(dipendente.luogonascita))
            self.tableWidget.setItem(self.i, 5, QTableWidgetItem(dipendente.abilitazione))
            self.tableWidget.setItem(self.i, 6, QTableWidgetItem(dipendente.email))
            self.i += 1

    def closeEvent(self, event):
        self.controller.save_data()