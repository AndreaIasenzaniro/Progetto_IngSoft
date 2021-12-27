from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListView, QVBoxLayout, QPushButton, QMessageBox, QTableWidgetItem, \
    QTableWidget, QHeaderView, QLabel

from listadipendenti.controller.ControlloreListaDipendenti import ControlloreListaDipendenti
from listadipendenti.views.VistaInserisciDipendente import VistaInserisciDipendente
from listadipendenti.views.VistaModificaDipendente import  VistaModificaDipendente


class VistaListaDipendenti(QWidget):
    def __init__(self, parent=None):
        super(VistaListaDipendenti, self).__init__(parent)

        self.showMaximized()
        #assegno il controllore della lista
        self.controller = ControlloreListaDipendenti()
        # creo tabella dei dipendenti
        self.create_table()
        self.list_view = self.tableWidget

        # definisco un layout orizzontale per la pagina
        h_layout = QHBoxLayout()
        # definisco un layout verticale per i pulsanti
        btn_layout = QVBoxLayout()

        image = QLabel(self)
        pixmap = QPixmap("listadipendenti/views/dipendenti.png")
        image.setPixmap(pixmap)
        image.show()

        # pulsante di apertura del dipendente
        btn_elimina = QPushButton("Elimina")
        btn_elimina.setStyleSheet("background-color: #f08080; font-size: 13px; font-weight: bold;")
        btn_elimina.clicked.connect(self.elimina_dipendente_click)
        # pulsante modifica del dipendente
        btn_modifica = QPushButton("Modifica")
        btn_modifica.setStyleSheet("background-color: #00bfff; font-size: 13px; font-weight: bold;")
        btn_modifica.clicked.connect(self.modifica_dipendente_click)
        # pulsante nuovo dipendente
        btn_nuovo = QPushButton("Nuovo")
        btn_nuovo.setStyleSheet("background-color: #90ee90; font-size: 13px; font-weight: bold;")
        btn_nuovo.clicked.connect(self.show_nuovo_dipendente_click)
        # pulsante di chiusura della finestra
        btn_esci = QPushButton("Esci")
        btn_esci.setStyleSheet("background-color: #66cdaa; font-size: 13px; font-weight: bold;")
        btn_esci.setShortcut("Esc")
        btn_esci.clicked.connect(self.funz_indietro)
        # aggiunta pulsanti al layout dei pulsanti
        btn_layout.addStretch()
        btn_layout.addWidget(btn_nuovo)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_modifica)
        btn_layout.addWidget(btn_elimina)
        btn_layout.addStretch()
        btn_layout.addWidget(btn_esci)

        h_layout.addLayout(btn_layout)
        h_layout.addWidget(self.tableWidget)
        # setting del layout della finestra
        self.setLayout(h_layout)
        self.setWindowTitle('Gestione Dipendenti')

    # visualizza finestra di inserimento di un nuovo dipendente
    def show_nuovo_dipendente_click(self):
        self.vista_inserisci_dipendente = VistaInserisciDipendente(self.controller, self.update_nuovo)
        self.vista_inserisci_dipendente.show()

    # visualizza finestra di modifica del dipendente selezionato
    def modifica_dipendente_click(self):
        try:
            # seleziono l'indice di riga della tabella
            selected = self.list_view.selectedIndexes()[0].row()
            dipendente_selezionato = self.controller.get_dipendente_by_index(selected)
            # creo la pagina di modifica con le info del dipendente selezionato
            self.vista_dipendente_mod = VistaModificaDipendente(dipendente_selezionato, self.controller, self.update_modifica)
            self.vista_dipendente_mod.show()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un dipendente da modificare.', QMessageBox.Ok, QMessageBox.Ok)

    # funzione di elimina del cliente selezionato
    def elimina_dipendente_click(self):
        try:
            self.selected = self.list_view.selectedIndexes()[0].row()
            dipendente_selezionato = self.controller.get_dipendente_by_index(self.selected)
            reply = QMessageBox.question(self, "Messaggio",
                                         "Sicuro di voler eliminare il dipendente selezionato? <p>OPERAZIONE IRREVERSIBILE",
                                         QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                from dipendente.controller.ControlloreDipendente import ControlloreDipendente
                # richiama funzione di elimina del controllore della lista
                self.controller.elimina_dipendente_by_id(ControlloreDipendente(dipendente_selezionato).get_id_dipendente())
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

    # tabella dei dipendenti
    def create_table(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.setRowCount(len(self.controller.get_lista_dipendenti()))
        self.tableWidget.setColumnCount(11)
        columns = ['Id', 'Cognome', 'Nome', 'Codice fiscale', 'Data di nascita', 'Luogo di nascita','Residenza','Indirizzo', 'Abilitazione', 'Telefono', 'Email']
        self.tableWidget.setHorizontalHeaderLabels(columns)

        self.controller.ordina_dipendenti(self.controller.get_lista_dipendenti())
        # popolo la tabella con i dipendenti nella lista
        self.i = 0
        for dipendente in self.controller.get_lista_dipendenti():
            self.tableWidget.setItem(self.i, 0, QTableWidgetItem(dipendente.id))
            self.tableWidget.setItem(self.i, 1, QTableWidgetItem(dipendente.cognome))
            self.tableWidget.setItem(self.i, 2, QTableWidgetItem(dipendente.nome))
            self.tableWidget.setItem(self.i, 3, QTableWidgetItem(dipendente.cf))
            self.tableWidget.setItem(self.i, 4, QTableWidgetItem(dipendente.data_nascita))
            self.tableWidget.setItem(self.i, 5, QTableWidgetItem(dipendente.luogo_nascita))
            self.tableWidget.setItem(self.i, 6, QTableWidgetItem(dipendente.residenza))
            self.tableWidget.setItem(self.i, 7, QTableWidgetItem(dipendente.indirizzo))
            self.tableWidget.setItem(self.i, 8, QTableWidgetItem(dipendente.abilitazione))
            self.tableWidget.setItem(self.i, 9, QTableWidgetItem(dipendente.telefono))
            self.tableWidget.setItem(self.i, 10, QTableWidgetItem(dipendente.email))
            self.i += 1
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    #aggiorna la tabella all'inserimento di un nuovo dipendente
    def update_nuovo(self):
        # conta dipendenti
        c = len(self.controller.get_lista_dipendenti())
        # aggiunge una riga
        self.tableWidget.setRowCount(c)
        self.controller.ordina_dipendenti(self.controller.get_lista_dipendenti())
        # inserimento dipendente nella tableWidget
        self.i = 0
        for dipendente in self.controller.get_lista_dipendenti():
            self.tableWidget.setItem(self.i, 0, QTableWidgetItem(dipendente.id))
            self.tableWidget.setItem(self.i, 1, QTableWidgetItem(dipendente.cognome))
            self.tableWidget.setItem(self.i, 2, QTableWidgetItem(dipendente.nome))
            self.tableWidget.setItem(self.i, 3, QTableWidgetItem(dipendente.cf))
            self.tableWidget.setItem(self.i, 4, QTableWidgetItem(dipendente.data_nascita))
            self.tableWidget.setItem(self.i, 5, QTableWidgetItem(dipendente.luogo_nascita))
            self.tableWidget.setItem(self.i, 6, QTableWidgetItem(dipendente.residenza))
            self.tableWidget.setItem(self.i, 7, QTableWidgetItem(dipendente.indirizzo))
            self.tableWidget.setItem(self.i, 8, QTableWidgetItem(dipendente.abilitazione))
            self.tableWidget.setItem(self.i, 9, QTableWidgetItem(dipendente.telefono))
            self.tableWidget.setItem(self.i, 10, QTableWidgetItem(dipendente.email))
            self.i += 1

    def update_modifica(self):
        # prendo la lista dei dipendenti ordinati per cognome
        self.controller.ordina_dipendenti(self.controller.get_lista_dipendenti())
        self.i = 0
        for dipendente in self.controller.get_lista_dipendenti():
            self.tableWidget.setItem(self.i, 0, QTableWidgetItem(dipendente.id))
            self.tableWidget.setItem(self.i, 1, QTableWidgetItem(dipendente.cognome))
            self.tableWidget.setItem(self.i, 2, QTableWidgetItem(dipendente.nome))
            self.tableWidget.setItem(self.i, 3, QTableWidgetItem(dipendente.cf))
            self.tableWidget.setItem(self.i, 4, QTableWidgetItem(dipendente.data_nascita))
            self.tableWidget.setItem(self.i, 5, QTableWidgetItem(dipendente.luogo_nascita))
            self.tableWidget.setItem(self.i, 6, QTableWidgetItem(dipendente.residenza))
            self.tableWidget.setItem(self.i, 7, QTableWidgetItem(dipendente.indirizzo))
            self.tableWidget.setItem(self.i, 8, QTableWidgetItem(dipendente.abilitazione))
            self.tableWidget.setItem(self.i, 9, QTableWidgetItem(dipendente.telefono))
            self.tableWidget.setItem(self.i, 10, QTableWidgetItem(dipendente.email))
            self.i += 1


    def funz_indietro(self):
        from home.views.VistaHome import VistaHome
        self.vista_home = VistaHome()
        self.close()
        return self.vista_home.show()

    # salvataggio dei cati alla chiusura della finestra
    def closeEvent(self, event):
        self.controller.save_data()