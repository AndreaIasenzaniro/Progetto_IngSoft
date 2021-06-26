from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox, QTableWidgetItem, QTableWidget

from listamovimenti.controller.ControlloreListaMovimenti import ControlloreListaMovimenti
from listamovimenti.views.VistaInserisciMovimento import VistaInserisciMovimento
from listamovimenti.views.VistaModificaMovimento import VistaModificaMovimentoCassa
from movimento.views.VistaMovimento import VistaMovimento


class VistaListaMovimenti(QWidget):
    def __init__(self, parent = None):
        super(VistaListaMovimenti, self).__init__(parent)

        self.controller = ControlloreListaMovimenti()

        self.v_layout = QVBoxLayout()

        self.create_table()
        self.list_view = self.tableWidget
        self.v_layout.addWidget(self.tableWidget)

        #self.update_ui()

        btn_apri = QPushButton("Apri")
        btn_apri.clicked.connect(self.show_movimento_selezionato_click)

        btn_modifica = QPushButton("Modifica")
        btn_modifica.clicked.connect(self.show_modifica_movimento_click)

        btn_nuovo = QPushButton("Nuovo")
        btn_nuovo.clicked.connect(self.show_nuovo_movimento_click)

        self.v_layout.addWidget(btn_nuovo)
        self.v_layout.addWidget(btn_modifica)
        self.v_layout.addWidget(btn_apri)

        self.setLayout(self.v_layout)

    def show_movimento_selezionato_click(self):
        #try:
            self.selected = self.list_view.selectedIndexes()[0].row()
            print(self.selected)
            movimento_selezionato = self.controller.get_movimento_by_index(self.selected)
            print(movimento_selezionato)
            self.vista_movimento = VistaMovimento(movimento_selezionato, self.controller.elimina_movimento_by_id, self.update_elimina)
            self.vista_movimento.show()
        #except:
            #QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un movimento da visualizzare.', QMessageBox.Ok,
                                 #QMessageBox.Ok)

    def create_table(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setRowCount(len(self.controller.get_lista_movimenti()))
        self.tableWidget.setColumnCount(3)
        columns = ['Data operaizone', 'Descrizione', 'Importo']
        self.tableWidget.setHorizontalHeaderLabels(columns)
        self.controller.oridna_movimenti(self.controller.get_lista_movimenti())
        self.i = 0
        for movimento in self.controller.get_lista_movimenti():
            #self.tableWidget.setItem(self.i, 0, QTableWidgetItem(movimento.id))
            self.tableWidget.setItem(self.i, 0, QTableWidgetItem(movimento.data_movimento))
            self.tableWidget.setItem(self.i, 1, QTableWidgetItem(movimento.descrizione))
            self.tableWidget.setItem(self.i, 2, QTableWidgetItem("€ {}".format(movimento.importo)))
            self.i += 1

    def update_elimina(self):
        riga = self.selected
        self.tableWidget.removeRow(riga)

    def show_modifica_movimento_click(self):
        try:
            selected = self.list_view.selectedIndexes()[0].row()
            movimento_selezionato = self.controller.get_movimento_by_index(selected)
            self.vista_movimento_modifica = VistaModificaMovimentoCassa(movimento_selezionato, self.controller, self.update_modifica)
            self.vista_movimento_modifica.show()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un movimento da modificare.', QMessageBox.Ok,
                                 QMessageBox.Ok)

    def show_nuovo_movimento_click(self):
        self.vista_inserisci_movimento = VistaInserisciMovimento(self.controller, self.update_nuovo)
        self.vista_inserisci_movimento.show()

    def update_nuovo(self):
        m = len(self.controller.get_lista_movimenti())
        self.tableWidget.setRowCount(m)
        self.controller.oridna_movimenti(self.controller.get_lista_movimenti())
        self.i=0
        for movimento in self.controller.get_lista_movimenti():
            #self.tableWidget.setItem(self.i, 0, QTableWidgetItem(movimento.id))
            self.tableWidget.setItem(self.i, 0, QTableWidgetItem(movimento.data_movimento))
            self.tableWidget.setItem(self.i, 1, QTableWidgetItem(movimento.descrizione))
            self.tableWidget.setItem(self.i, 2, QTableWidgetItem("€ {}".format(movimento.importo)))
            self.i += 1

    def update_modifica(self):
        self.controller.oridna_movimenti(self.controller.get_lista_movimenti())
        self.i=0
        for movimento in self.controller.get_lista_movimenti():
            #self.tableWidget.setItem(self.i, 0, QTableWidgetItem(movimento.id))
            self.tableWidget.setItem(self.i, 0, QTableWidgetItem(movimento.data_movimento))
            self.tableWidget.setItem(self.i, 1, QTableWidgetItem(movimento.descrizione))
            self.tableWidget.setItem(self.i, 2, QTableWidgetItem("€ {}".format(movimento.importo)))
            self.i += 1

    def update_elimina(self):
        row = self.selected
        self.tableWidget.removeRow(row)

    def closeEvent(self, event):
        self.controller.save_data()