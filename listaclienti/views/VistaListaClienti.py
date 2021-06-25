from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListView, QVBoxLayout, QPushButton, QMessageBox, QTableWidget, \
    QTableWidgetItem, QHeaderView, QTableView
from PyQt5.QtCore import Qt

from cliente.views.VistaCliente import VistaCliente
from listaclienti.controller.ControlloreListaClienti import ControlloreListaClienti
from listaclienti.views.VistaInserisciCliente import VistaInserisciCliente
from listaclienti.views.VistaModificaCliente import VistaModificaCliente


class VistaListaClienti(QWidget):
    def __init__(self, parent=None):
        super(VistaListaClienti, self).__init__(parent)

        self.setFixedSize(850, 550)
        self.move(300, 100)

        self.controller = ControlloreListaClienti()

        self.h_layout = QHBoxLayout()

        #crea tabella
        self.createTable()
        #per non modificare self.list_view in table_view
        self.list_view = self.tableWidget
        self.h_layout.addWidget(self.tableWidget)

        buttons_layout = QVBoxLayout()
        open_button = QPushButton("Apri")
        #open_button.setStyleSheet("background-color: cyan; font-size: 15px; font-weight: bold;")
        open_button.clicked.connect(self.show_selected_info_click)
        buttons_layout.addWidget(open_button)

        edit_button = QPushButton("Modifica")
        #edit_button.setStyleSheet("background-color: green; font-size: 15px; font-weight: bold;")
        edit_button.clicked.connect(self.show_modifica_cliente_click)
        buttons_layout.addWidget(edit_button)

        new_button = QPushButton("Nuovo")
        #new_button.setStyleSheet("background-color: #00ff00; font-size: 15px; font-weight: bold;")
        new_button.clicked.connect(self.show_nuovo_cliente_click)
        buttons_layout.addWidget(new_button)
        buttons_layout.addStretch()


        # creazione pulsante di chiusura della finestra
        btn_esci = QPushButton("Esci")
        btn_esci.setShortcut("Esc")
        btn_esci.clicked.connect(self.funz_indietro)
        buttons_layout.addWidget(btn_esci)

        self.h_layout.addLayout(buttons_layout)

        self.setLayout(self.h_layout)
        self.setWindowTitle("Lista Clienti")

    def show_selected_info_click(self):
        try:
            self.selected = self.list_view.selectedIndexes()[0].row()
            cliente_selezionato = self.controller.get_cliente_by_index(self.selected)
            self.vista_cliente = VistaCliente(cliente_selezionato, self.controller.elimina_cliente_by_id, self.update_elimina)
            self.vista_cliente.show()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un cliente da visualizzare.', QMessageBox.Ok, QMessageBox.Ok)


    def show_modifica_cliente_click(self):
        try:
            self.selected_mod = self.list_view.selectedIndexes()[0].row()
            cliente_selezionato = self.controller.get_cliente_by_index(self.selected_mod)
            self.vista_cliente_mod = VistaModificaCliente(cliente_selezionato, self.controller, self.update_mod)
            self.vista_cliente_mod.show()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un cliente da modificare.', QMessageBox.Ok, QMessageBox.Ok)


    def show_nuovo_cliente_click(self):
        self.vista_inserisci_cliente = VistaInserisciCliente(self.controller, self.update_new)
        self.vista_inserisci_cliente.show()

    def funz_indietro(self):
        from home.views.VistaHome import VistaHome
        self.vista_home = VistaHome()
        self.close()
        return self.vista_home.show()

    def closeEvent(self, event):
        self.controller.saveData()

    #Create table
    def createTable(self):
        self.tableWidget = QTableWidget()
        # Row count
        self.tableWidget.setRowCount(len(self.controller.get_lista_dei_clienti()))
        # Column count
        self.tableWidget.setColumnCount(5)
        columns = ['Cognome', 'Nome', 'Codice fiscale', 'Abbonamento', 'Certificato']
        self.tableWidget.setHorizontalHeaderLabels(columns)
        self.controller.cliente_ordinato(self.controller.get_lista_dei_clienti())

        #inserimento clienti nella tableWidget
        self.i = 0
        for cliente in self.controller.get_lista_dei_clienti():
            self.tableWidget.setItem(self.i, 0, QTableWidgetItem(cliente.cognome))
            self.tableWidget.setItem(self.i, 1, QTableWidgetItem(cliente.nome))
            self.tableWidget.setItem(self.i, 2, QTableWidgetItem(cliente.cf))
            if cliente.getAbbonamento() is not None:
                self.tableWidget.setItem(self.i, 3, QTableWidgetItem("In corso"))
            else:
                self.tableWidget.setItem(self.i, 3, QTableWidgetItem("Scaduto"))
            if cliente.getCertificato() is not None:
                self.tableWidget.setItem(self.i, 4, QTableWidgetItem("In corso"))
            else:
                self.tableWidget.setItem(self.i, 4, QTableWidgetItem("Scaduto"))
            self.i += 1

        # Table will fit the screen horizontally
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def update_elimina(self):
        riga = self.selected
        self.tableWidget.removeRow(riga)

    def update_new(self):
        #count ultimo cliente
        c = len(self.controller.get_lista_dei_clienti())
        #aggiungi una riga
        self.tableWidget.setRowCount(c)
        self.controller.cliente_ordinato(self.controller.get_lista_dei_clienti())
        # inserimento clienti nella tableWidget
        self.i = 0
        for cliente in self.controller.get_lista_dei_clienti():
            self.tableWidget.setItem(self.i, 0, QTableWidgetItem(cliente.cognome))
            self.tableWidget.setItem(self.i, 1, QTableWidgetItem(cliente.nome))
            self.tableWidget.setItem(self.i, 2, QTableWidgetItem(cliente.cf))
            if cliente.getAbbonamento() is not None:
                self.tableWidget.setItem(self.i, 3, QTableWidgetItem("In corso"))
            else:
                self.tableWidget.setItem(self.i, 3, QTableWidgetItem("Scaduto"))
            if cliente.getCertificato() is not None:
                self.tableWidget.setItem(self.i, 4, QTableWidgetItem("In corso"))
            else:
                self.tableWidget.setItem(self.i, 4, QTableWidgetItem("Scaduto"))
            self.i += 1

    def update_mod(self):
        self.controller.cliente_ordinato(self.controller.get_lista_dei_clienti())
        # inserimento clienti nella tableWidget
        self.i = 0
        for cliente in self.controller.get_lista_dei_clienti():
            self.tableWidget.setItem(self.i, 0, QTableWidgetItem(cliente.cognome))
            self.tableWidget.setItem(self.i, 1, QTableWidgetItem(cliente.nome))
            self.tableWidget.setItem(self.i, 2, QTableWidgetItem(cliente.cf))
            self.i += 1