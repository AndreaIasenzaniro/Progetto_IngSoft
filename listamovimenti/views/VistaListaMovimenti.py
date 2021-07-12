from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QMessageBox, QTableWidgetItem, QTableWidget, QLabel, \
    QSizePolicy, QHeaderView, QHBoxLayout

from listamovimenti.controller.ControlloreListaMovimenti import ControlloreListaMovimenti
from listamovimenti.views.VistaInserisciMovimento import VistaInserisciMovimento
from listamovimenti.views.VistaModificaMovimento import VistaModificaMovimentoCassa
from movimento.views.VistaMovimento import VistaMovimento


class VistaListaMovimenti(QWidget):
    def __init__(self, parent = None):
        super(VistaListaMovimenti, self).__init__(parent)

        self.update()

        self.setFixedSize(800, 500)
        self.move(250, 100)

        self.controller = ControlloreListaMovimenti()
        self.h_layout = QHBoxLayout()
        self.v_lay_sx = QVBoxLayout()
        self.v_lay_dx = QVBoxLayout()
        self.create_table()
        self.list_view = self.tableWidget
        self.saldo = self.controller.get_saldo()

        self.label_saldo = QLabel("Saldo attuale: {}".format(self.saldo))
        font = QtGui.QFont()
        font.setPointSize(11)
        font.setBold(True)
        self.label_saldo.setFont(font)
        if self.controller.get_saldo() < 0.0:
            self.label_saldo.setStyleSheet('color: red')
        else:
            self.label_saldo.setStyleSheet('color: green')

        btn_elimina = QPushButton("Elimina")
        btn_elimina.clicked.connect(self.elimina_movimento_click)
        btn_modifica = QPushButton("Modifica")
        btn_modifica.clicked.connect(self.show_modifica_movimento_click)
        btn_nuovo = QPushButton("Nuovo")
        btn_nuovo.clicked.connect(self.show_nuovo_movimento_click)
        btn_esc = QPushButton("Esci")
        btn_esc.clicked.connect(self.funz_esci)

        self.v_lay_sx.addStretch()
        self.v_lay_sx.addWidget(btn_nuovo)
        self.v_lay_sx.addWidget(btn_modifica)
        self.v_lay_sx.addWidget(btn_elimina)
        self.v_lay_sx.addStretch()
        self.v_lay_sx.addWidget(btn_esc)

        self.v_lay_dx.addWidget(self.label_saldo)
        self.v_lay_dx.addWidget(self.tableWidget)

        self.h_layout.addLayout(self.v_lay_sx)
        self.h_layout.addLayout(self.v_lay_dx)

        self.setLayout(self.h_layout)

    # funzione pulsante modifica
    def show_modifica_movimento_click(self):
        try:
            selected = self.list_view.selectedIndexes()[0].row()
            movimento_selezionato = self.controller.get_movimento_by_index(selected)
            self.vista_movimento_modifica = VistaModificaMovimentoCassa(movimento_selezionato, self.controller, self.update_modifica)
            self.vista_movimento_modifica.show()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un movimento da modificare.', QMessageBox.Ok,
                                 QMessageBox.Ok)
    # funzione pulsante elimina
    def elimina_movimento_click(self):
        self.selected = self.list_view.selectedIndexes()[0].row()
        movimento_selezionato = self.controller.get_movimento_by_index(self.selected)
        from movimento.controller.ControlloreMovimento import ControlloreMovimento
        self.controller.elimina_movimento_by_id(ControlloreMovimento(movimento_selezionato).get_id_movimento())
        row = self.selected
        self.tableWidget.removeRow(row)
        self.update()
    #funzione pulsante apri
    def show_movimento_selezionato_click(self):
        try:
            self.selected = self.list_view.selectedIndexes()[0].row()
            movimento_selezionato = self.controller.get_movimento_by_index(self.selected)
            self.vista_movimento = VistaMovimento(movimento_selezionato, self.controller.elimina_movimento_by_id, self.update_elimina)
            self.vista_movimento.show()
        except:
            QMessageBox.critical(self, 'Errore', 'Per favore, seleziona un movimento da visualizzare.', QMessageBox.Ok,
                                 QMessageBox.Ok)
    # funzione pulsante nuovo
    def show_nuovo_movimento_click(self):
        self.vista_inserisci_movimento = VistaInserisciMovimento(self.controller, self.update_nuovo)
        self.vista_inserisci_movimento.show()

    def create_table(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        self.tableWidget.setRowCount(len(self.controller.get_lista_movimenti()))
        self.tableWidget.setColumnCount(4)
        columns = ['Data operaizone', 'Causale', 'Descrizione', 'Importo']
        self.tableWidget.setHorizontalHeaderLabels(columns)
        header = self.tableWidget.horizontalHeader()
        header.setSectionResizeMode(QHeaderView.ResizeToContents)
        self.controller.oridna_movimenti(self.controller.get_lista_movimenti())
        self.i = 0
        for movimento in self.controller.get_lista_movimenti():
            self.tableWidget.setItem(self.i, 0, QTableWidgetItem(movimento.data))
            self.tableWidget.setItem(self.i, 1, QTableWidgetItem(movimento.causale))
            self.tableWidget.setItem(self.i, 2, QTableWidgetItem(movimento.descrizione))
            self.tableWidget.setItem(self.i, 3, QTableWidgetItem("€ {}".format(movimento.importo)))
            self.i += 1
        self.tableWidget.horizontalHeader().setStretchLastSection(True)

    def update_nuovo(self):
        m = len(self.controller.get_lista_movimenti())
        self.tableWidget.setRowCount(m)
        self.controller.oridna_movimenti(self.controller.get_lista_movimenti())
        self.i=0
        for movimento in self.controller.get_lista_movimenti():
            self.tableWidget.setItem(self.i, 0, QTableWidgetItem(movimento.data))
            self.tableWidget.setItem(self.i, 1, QTableWidgetItem(movimento.causale))
            self.tableWidget.setItem(self.i, 2, QTableWidgetItem(movimento.descrizione))
            self.tableWidget.setItem(self.i, 3, QTableWidgetItem("€ {}".format(movimento.importo)))
            self.i += 1
        self.update()

    def update_modifica(self):
        self.controller.oridna_movimenti(self.controller.get_lista_movimenti())
        self.i=0
        for movimento in self.controller.get_lista_movimenti():
            self.tableWidget.setItem(self.i, 0, QTableWidgetItem(movimento.data))
            self.tableWidget.setItem(self.i, 1, QTableWidgetItem(movimento.causale))
            self.tableWidget.setItem(self.i, 2, QTableWidgetItem(movimento.descrizione))
            self.tableWidget.setItem(self.i, 3, QTableWidgetItem("€ {}".format(movimento.importo)))
            self.i += 1

    def closeEvent(self, event):
        self.controller.save_data()

    def funz_esci(self):
        from home.views.VistaHome import VistaHome
        self.close()
        self.home = VistaHome()
        return self.home.show()