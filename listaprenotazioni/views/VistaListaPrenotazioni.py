from PyQt5.QtGui import QStandardItemModel, QStandardItem, QBrush
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QListView, QVBoxLayout, QPushButton, QMessageBox
from PyQt5.QtCore import Qt

from listaprenotazioni.controller.ControlloreListaPrenotazioni import ControlloreListaPrenotazioni
from listaprenotazioni.views.VistaInserisciPrenotazione import VistaInserisciPrenotazione
from prenotazione.views.VistaPrenotazione import VistaPrenotazione


class VistaListaPrenotazioni(QWidget):
    def __init__(self, data_selezionata, parent=None):
        super(VistaListaPrenotazioni, self).__init__(parent)
        self.controller = ControlloreListaPrenotazioni()
        self.data_selezionata=data_selezionata
        h_layout = QHBoxLayout()
        self.list_view = QListView()
        self.update_ui()
        h_layout.addWidget(self.list_view)
        #self.stampa_lista()
        buttons_layout = QVBoxLayout()
        open_button = QPushButton('Apri')
        open_button.clicked.connect(self.show_selected_info)
        buttons_layout.addWidget(open_button)
        buttons_layout.addStretch()
        h_layout.addLayout(buttons_layout)
        self.setLayout(h_layout)
        self.resize(600,300)
        self.setWindowTitle('Lista Prenotazioni' + " " + self.data_selezionata)
        self.controller.save_data()
    def update_ui(self):
        self.listview_model = QStandardItemModel(self.list_view)
        self.i=0
        self.lista_selezionata = []
        for prenotazione in self.controller.get_lista_prenotazioni():
            from home.views.VistaHome import VistaHome
            if prenotazione.campo.tipo == VistaHome.selezione_campo and prenotazione.data == self.data_selezionata:
                self.lista_selezionata.append(prenotazione)
            else:
                pass
            self.controller.ordina(self.lista_selezionata)
        for prenotazione in self.lista_selezionata:
            item = QStandardItem()
            item.setText(prenotazione.data + " " + prenotazione.ora_inizio + " " + prenotazione.ora_fine + " " + prenotazione.cognome + " " + prenotazione.nome + " " + str(prenotazione.id))
            item.setEditable(False)
            if self.i%2:
                item.setBackground(QBrush(Qt.lightGray))
            font = item.font()
            font.setPointSize(12)
            item.setFont(font)
            self.listview_model.appendRow(item)
        self.list_view.setModel(self.listview_model)
    def show_selected_info(self):
        #try:
            selected = self.list_view.selectedIndexes()[0].row()
            prenotazione_selezionata = self.lista_selezionata[selected]
            self.vista_prenotazione = VistaPrenotazione(prenotazione_selezionata, self.controller.elimina_prenotazione_by_id, self.update_ui)
            self.vista_prenotazione.show()
        #except:
            #QMessageBox.critical(self, 'Errore', 'Per favore, seleziona una prenotazione da visualizzare.', QMessageBox.Ok,QMessageBox.Ok)
    def get_lista_index(self, index, lista):
        return lista[index]
    def closeEvent(self, event):
        self.controller.save_data()