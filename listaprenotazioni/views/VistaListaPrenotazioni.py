from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QMessageBox, QTableWidget, \
    QTableWidgetItem, QHeaderView

from listamovimenti.controller.ControlloreListaMovimenti import ControlloreListaMovimenti
from listaprenotazioni.controller.ControlloreListaPrenotazioni import ControlloreListaPrenotazioni
from listaprenotazioni.views.VistaModificaPrenotazione import VistaModificaPrenotazione
from movimento.model.Movimento import Movimento
from prenotazione.controller.ControllorePrenotazione import ControllorePrenotazione
from prenotazione.views.VistaPrenotazione import VistaPrenotazione


class VistaListaPrenotazioni(QWidget):
    def __init__(self, data_selezionata, parent=None):
        super(VistaListaPrenotazioni, self).__init__(parent)
        self.controller = ControlloreListaPrenotazioni()
        self.data_selezionata=data_selezionata
        self.controlloreMov = ControlloreListaMovimenti()
        self.controllorePre = ControlloreListaPrenotazioni()

        self.setWindowTitle("Prenotazioni del {}".format(data_selezionata))
        h_layout = QHBoxLayout()
        self.createTable()
        self.list_view = self.tableWidget
        h_layout.addWidget(self.list_view)
        buttons_layout = QVBoxLayout()
        buttons_layout.addStretch()
        btn_disdici = QPushButton("Elimina")
        btn_disdici.setStyleSheet("background-color: #f08080; font-size: 13px; font-weight: bold;")
        btn_disdici.clicked.connect(self.elimina_prenotazione_click)
        buttons_layout.addWidget(btn_disdici)
        btn_modifica = QPushButton('Modifica')
        btn_modifica.setStyleSheet("background-color: #00bfff; font-size: 13px; font-weight: bold;")
        btn_modifica.clicked.connect(self.modifica_prenotazione_click)
        buttons_layout.addWidget(btn_modifica)
        btn_esci = QPushButton('Esci')
        btn_esci.setStyleSheet("background-color: #66cdaa; font-size: 13px; font-weight: bold;")
        btn_esci.clicked.connect(self.funz_esci)
        buttons_layout.addStretch()
        buttons_layout.addWidget(btn_esci)
        h_layout.addLayout(buttons_layout)
        self.setLayout(h_layout)
        self.resize(1100, 600)
        self.controller.save_data()

    def elimina_prenotazione_click(self):
        try:
            self.selected = self.list_view.selectedIndexes()[0].row()
            prenotazione_selezionata = self.lista_selezionata[self.selected]
            controller = ControllorePrenotazione(prenotazione_selezionata)
            reply = QMessageBox.question(self, "Messaggio",
                                         "Sicuro di voler eliminare il dipendente selezionato? <p>OPERAZIONE IRREVERSIBILE",
                                         QMessageBox.Yes |
                                         QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.controller.elimina_prenotazione_by_id(controller.get_id_prenotazione())
                riga = self.selected
                self.tableWidget.removeRow(riga)
                # aggiornamento
                self.controllorePre.save_data()
                # emetto uscita di cassa per disdetta prenotazione
                self.movimento = Movimento(controller.get_data_prenotazione(), "Disdetta campo da " + str(
                    controller.get_campo_tipo()) + " - ID prenotazione: " + str(controller.get_id_prenotazione()), "Spesa",
                                           controller.prezzi_campi())
                self.controlloreMov.aggiungi_movimento(self.movimento)
                self.controlloreMov.save_data()
            else:
                pass
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un movimento da eliminare.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def visualizza_prenotazione_click(self):
        try:
            self.selected = self.list_view.selectedIndexes()[0].row()
            prenotazione_selezionata = self.lista_selezionata[self.selected]
            self.vista_prenotazione = VistaPrenotazione(prenotazione_selezionata, self.controller.elimina_prenotazione_by_id, self.update_elimina)
            self.vista_prenotazione.show()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona una prenotazione da visualizzare.', QMessageBox.Ok,QMessageBox.Ok)

    def modifica_prenotazione_click(self):
        try:
            self.close()
            self.selected = self.list_view.selectedIndexes()[0].row()
            prenotazione_selezionata = self.lista_selezionata[self.selected]
            self.modifica_prenotazione = VistaModificaPrenotazione(prenotazione_selezionata, self.controller, self.update_mod)
            self.modifica_prenotazione.show()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona una prenotazione da visualizzare.', QMessageBox.Ok,QMessageBox.Ok)

    def get_lista_index(self, index, lista):
        return lista[index]

    def closeEvent(self, event):
        self.controller.save_data()

    #Create table
    def createTable(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        # Row count
        rows = 0
        self.tableWidget.setRowCount(len(self.controller.get_lista_prenotazioni()))
        # Column count
        self.tableWidget.setColumnCount(8)
        columns = ['Cognome', 'Nome', 'Documento', 'Campo', 'Numero', 'Data', 'Ora inizio', 'Ora fine']
        self.tableWidget.setHorizontalHeaderLabels(columns)
        self.controller.ordina(self.controller.get_lista_prenotazioni())
        #inserimento prenotazioni nella tableWidget
        self.i = 0
        self.lista_selezionata = []
        for prenotazione in self.controller.get_lista_prenotazioni():
            from home.views.VistaHome import VistaHome
            if prenotazione.campo.tipo == VistaHome.selezione_campo and prenotazione.data == self.data_selezionata:
                self.lista_selezionata.append(prenotazione)
            else:
                pass
            self.controller.ordina(self.lista_selezionata)
        for prenotazione in self.lista_selezionata:
            self.tableWidget.setItem(self.i, 0, QTableWidgetItem(prenotazione.cognome))
            self.tableWidget.setItem(self.i, 1, QTableWidgetItem(prenotazione.nome))
            self.tableWidget.setItem(self.i, 2, QTableWidgetItem(prenotazione.documento))
            self.tableWidget.setItem(self.i, 3, QTableWidgetItem(prenotazione.campo.tipo))
            self.tableWidget.setItem(self.i, 4, QTableWidgetItem(prenotazione.campo.numero))
            self.tableWidget.setItem(self.i, 5, QTableWidgetItem(prenotazione.data))
            self.tableWidget.setItem(self.i, 6, QTableWidgetItem(prenotazione.ora_inizio))
            self.tableWidget.setItem(self.i, 7, QTableWidgetItem(prenotazione.ora_fine))
            self.i += 1
            rows += 1
        #risetto le prenotazioni di un giorno specifico
        self.tableWidget.setRowCount(rows)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

    def update_mod(self):
        self.controller.ordina(self.controller.get_lista_prenotazioni())
        # inserimento prenotazioni nella tableWidget
        self.i = 0
        for prenotazione in self.controller.get_lista_prenotazioni():
            self.tableWidget.setItem(self.i, 0, QTableWidgetItem(prenotazione.cognome))
            self.tableWidget.setItem(self.i, 1, QTableWidgetItem(prenotazione.nome))
            self.tableWidget.setItem(self.i, 2, QTableWidgetItem(prenotazione.documento))
            self.i += 1

    def funz_esci(self):
        self.close()
        from calendario.Calendario import Calendario
        Calendario.vista_prenotazione = False