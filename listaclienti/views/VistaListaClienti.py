from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QMessageBox, QTableWidget, QTableWidgetItem, \
    QHeaderView, QLabel

from cliente.views.VistaCliente import VistaCliente
from listaclienti.controller.ControlloreListaClienti import ControlloreListaClienti
from listaclienti.views.VistaInserisciCliente import VistaInserisciCliente
from listaclienti.views.VistaModificaCliente import VistaModificaCliente


class VistaListaClienti(QWidget):
    profilo_cliente = False
    def __init__(self, parent=None):
        super(VistaListaClienti, self).__init__(parent)

        self.showMaximized()
        # assegno il controllore della lista
        self.controller = ControlloreListaClienti()
        # creo tabella dei clienti
        self.create_table()
        self.list_view = self.tableWidget

        self.h_layout = QHBoxLayout()
        buttons_layout = QVBoxLayout()
        self.profilo_cliente = QVBoxLayout()
        image = QLabel(self)
        pixmap = QPixmap("listaclienti/views/palestra.png")
        image.setPixmap(pixmap)
        image.show()

        # pulsante di apertura del cliente
        btn_apri = QPushButton("Apri")
        btn_apri.setStyleSheet("background-color: #b0c4de; font-size: 13px; font-weight: bold;")
        btn_apri.clicked.connect(self.show_cliente_selezionato_click)
        # pulsante di modifica del cliente
        btn_modifica = QPushButton("Modifica")
        btn_modifica.setStyleSheet("background-color: #00bfff; font-size: 13px; font-weight: bold;")
        btn_modifica.clicked.connect(self.show_modifica_cliente_click)
        # pulsante nuovo cliente
        btn_nuovo = QPushButton("Nuovo")
        btn_nuovo.setStyleSheet("background-color: #90ee90; font-size: 13px; font-weight: bold;")
        btn_nuovo.clicked.connect(self.show_nuovo_cliente_click)
        # pulsante di elimina del cliente
        btn_elimina = QPushButton("Elimina")
        btn_elimina.setStyleSheet("background-color: #f08080; font-size: 13px; font-weight: bold;")
        btn_elimina.clicked.connect(self.elimina_cliente_click)
        # pulsante di chiusura della finestra
        btn_esci = QPushButton("Esci")
        btn_esci.setShortcut("Esc")
        btn_esci.setStyleSheet("background-color: #66cdaa; font-size: 13px; font-weight: bold;")
        btn_esci.clicked.connect(self.funz_esci)
        # aggiunta pulsanti al layout dei pulsanti
        buttons_layout.addStretch()
        buttons_layout.addWidget(btn_nuovo)
        buttons_layout.addStretch()
        buttons_layout.addWidget(btn_apri)
        buttons_layout.addWidget(btn_modifica)
        buttons_layout.addWidget(btn_elimina)
        buttons_layout.addStretch()
        buttons_layout.addWidget(btn_esci)

        self.h_layout.addLayout(buttons_layout)
        self.h_layout.addWidget(self.tableWidget)
        # setting del layout della finestra
        self.setLayout(self.h_layout)
        self.setWindowTitle("Lista Clienti")

    # visualizza scheda cliente selezionato
    def show_cliente_selezionato_click(self):
        try:
            # seleziono l'indice di riga della tabella
            self.selected = self.tableWidget.selectedIndexes()[0].row()
            # seleziono il cliente per indice
            cliente_selezionato = self.controller.get_cliente_by_index(self.selected)
            # creo la vista del cliente selezionato
            self.vista_cliente = VistaCliente(cliente_selezionato, self.controller.elimina_cliente_by_id, self.update_elimina)
            # utilizzando una variabile globale apro la vista del cliente
            if VistaListaClienti.profilo_cliente == False:
                self.profilo_cliente.addWidget(self.vista_cliente)
                self.h_layout.addLayout(self.profilo_cliente)
                VistaListaClienti.profilo_cliente = True
            # se la vista esiste già non viene aperta una nuova
            elif VistaListaClienti.profilo_cliente == True:
                pass
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un cliente da visualizzare.', QMessageBox.Ok, QMessageBox.Ok)

    # visualizza finestra di inserimento di un nuovo cliente
    def show_nuovo_cliente_click(self):
        self.vista_inserisci_cliente = VistaInserisciCliente(self.controller, self.update_nuovo)
        self.vista_inserisci_cliente.show()

    # visualizza finestra di modifica del cliente selezionato
    def show_modifica_cliente_click(self):
        try:
            # seleziono l'indice di riga della tabella
            self.selected_mod = self.list_view.selectedIndexes()[0].row()
            cliente_selezionato = self.controller.get_cliente_by_index(self.selected_mod)
            # creo la pagina di modifica con le info del cliente selezionato
            self.vista_cliente_mod = VistaModificaCliente(cliente_selezionato, self.controller, self.update_modifica)
            self.vista_cliente_mod.show()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un cliente da modificare.', QMessageBox.Ok, QMessageBox.Ok)

    # funzione di elimina del cliente selezionato
    def elimina_cliente_click(self):
        try:
            self.selected = self.list_view.selectedIndexes()[0].row()
            cliente_selezionato = self.controller.get_cliente_by_index(self.selected)
            reply = QMessageBox.question(self, "Messaggio",
                                         "Sicuro di voler eliminare il dipendente selezionato? <p>OPERAZIONE IRREVERSIBILE",
                                         QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                from cliente.controller.ControlloreCliente import ControlloreCliente
                # richiama funzione di elimina del controllore della lista
                self.controller.elimina_cliente_by_id(ControlloreCliente(cliente_selezionato).get_id_cliente())
                self.update_elimina()
            else:
                pass
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un movimento da eliminare.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def update_elimina(self):
        riga = self.selected
        self.tableWidget.removeRow(riga)
        self.update()

    # tabella dei clienti
    def create_table(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.setRowCount(len(self.controller.get_lista_dei_clienti()))
        self.tableWidget.setColumnCount(5)
        columns = ['Cognome', 'Nome', 'Codice fiscale', 'Abbonamento', 'Certificato']
        self.tableWidget.setHorizontalHeaderLabels(columns)
        self.controller.cliente_ordinato(self.controller.get_lista_dei_clienti())
        # popolo la tabella con i clienti nella lista
        self.i = 0
        for cliente in self.controller.get_lista_dei_clienti():
            self.tableWidget.setItem(self.i, 0, QTableWidgetItem(cliente.cognome))
            self.tableWidget.setItem(self.i, 1, QTableWidgetItem(cliente.nome))
            self.tableWidget.setItem(self.i, 2, QTableWidgetItem(cliente.cf))
            if cliente.get_abbonamento() is not None:
                self.tableWidget.setItem(self.i, 3, QTableWidgetItem("In corso"))
            else:
                self.tableWidget.setItem(self.i, 3, QTableWidgetItem("Scaduto"))
                self.tableWidget.item(self.i, 3).setForeground(QtGui.QColor(255, 127, 127))

            if cliente.get_certificato() is not None:
                self.tableWidget.setItem(self.i, 4, QTableWidgetItem("Valido"))
            else:
                self.tableWidget.setItem(self.i, 4, QTableWidgetItem("Scaduto"))
                self.tableWidget.item(self.i, 4).setForeground(QtGui.QColor(255, 127, 127))

            self.i += 1
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    # aggiorna la tabella all'inserimento di un nuovo cliente
    def update_nuovo(self):
        # conta clienti
        c = len(self.controller.get_lista_dei_clienti())
        # aggiungi una riga
        self.tableWidget.setRowCount(c)
        self.controller.cliente_ordinato(self.controller.get_lista_dei_clienti())
        # inserimento clienti nella tableWidget
        self.i = 0
        for cliente in self.controller.get_lista_dei_clienti():
            self.tableWidget.setItem(self.i, 0, QTableWidgetItem(cliente.cognome))
            self.tableWidget.setItem(self.i, 1, QTableWidgetItem(cliente.nome))
            self.tableWidget.setItem(self.i, 2, QTableWidgetItem(cliente.cf))
            if cliente.get_abbonamento() is not None:
                self.tableWidget.setItem(self.i, 3, QTableWidgetItem("In corso"))
            else:
                self.tableWidget.setItem(self.i, 3, QTableWidgetItem("Scaduto"))
                self.tableWidget.item(self.i, 3).setForeground(QtGui.QColor(255, 127, 127))
            if cliente.get_certificato() is not None:
                self.tableWidget.setItem(self.i, 4, QTableWidgetItem("Valido"))
            else:
                self.tableWidget.setItem(self.i, 4, QTableWidgetItem("Scaduto"))
                self.tableWidget.item(self.i, 4).setForeground(QtGui.QColor(255, 127, 127))
            self.i += 1

    def update_modifica(self):
        # prendo la lista dei clienti ordinata per cognome
        self.controller.cliente_ordinato(self.controller.get_lista_dei_clienti())
        self.i = 0
        for cliente in self.controller.get_lista_dei_clienti():
            self.tableWidget.setItem(self.i, 0, QTableWidgetItem(cliente.cognome))
            self.tableWidget.setItem(self.i, 1, QTableWidgetItem(cliente.nome))
            self.tableWidget.setItem(self.i, 2, QTableWidgetItem(cliente.cf))
            self.i += 1

    def funz_esci(self):
        from home.views.VistaHome import VistaHome
        self.vista_home = VistaHome()
        self.close()
        # alla chiusura della finestra setto la variabie globale della vista del cliente su false
        VistaListaClienti.profilo_cliente = False
        return self.vista_home.show()

    # salvataggio dei cati alla chiusura della finestra
    def closeEvent(self, event):
        self.controller.save_data()