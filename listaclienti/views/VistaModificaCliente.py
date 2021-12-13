from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QLabel, QLineEdit, QMessageBox, \
    QHBoxLayout

from cliente.controller.ControlloreCliente import ControlloreCliente
from cliente.model.Cliente import Cliente


class VistaModificaCliente(QWidget):
    def __init__(self, cliente_selezionato, controller, callback):
        super(VistaModificaCliente, self).__init__()
        self.cl = cliente_selezionato
        self.cliente = ControlloreCliente(cliente_selezionato)
        self.controller = controller
        self.callback = callback
        # dizionario vuoto
        self.info = {}

        #layout di modifica dei dati del cliente
        self.v_layout = QVBoxLayout()
        self.setFixedSize(630, 370)

        btn_modifica = QPushButton("Modifica")
        btn_modifica.setStyleSheet("background-color: #90ee90; font-size: 13px; font-weight: bold;")
        btn_modifica.clicked.connect(self.mod_cliente)

        btn_annulla = QPushButton("Annulla")
        btn_annulla.setStyleSheet("background-color: #f08080; font-size: 13px; font-weight: bold;")
        btn_annulla.clicked.connect(self.close)

        self.label_img = QLabel()
        self.label_img.setPixmap(QPixmap('listaclienti/data/utente.png'))

        h_lay_sup = QHBoxLayout()
        v_lay_sup_sx = QVBoxLayout()
        v_lay_sup_dx = QVBoxLayout()
        v_lay_sup_sx.addStretch()
        v_lay_sup_sx.addLayout(self.get_label_line("Nome", self.cliente.get_nome_cliente(), "Nome"))
        v_lay_sup_sx.addLayout(self.get_label_line("Cognome", self.cliente.get_cognome_cliente(), "Cognome"))
        v_lay_sup_sx.addLayout(self.get_label_line("Codice Fiscale", self.cliente.get_cf_cliente(), "Codice Fiscale"))
        v_lay_sup_sx.addStretch()
        v_lay_sup_dx.addWidget(self.label_img)
        h_lay_sup.addLayout(v_lay_sup_sx)
        h_lay_sup.addLayout(v_lay_sup_dx)

        h_lay_inf = QHBoxLayout()
        v_lay_inf_sx = QVBoxLayout()
        v_lay_inf_dx = QVBoxLayout()
        v_lay_inf_sx.addLayout(self.get_label_line("Luogo di nascita", self.cliente.get_luogo_nascita_cliente(), "Nato a"))
        v_lay_inf_dx.addLayout(self.get_label_line("Data di nascita", self.cliente.get_data_nascita_cliente(), "il"))
        v_lay_inf_sx.addLayout(self.get_label_line("Residenza", self.cliente.get_residenza_cliente(), "Residente a"))
        v_lay_inf_dx.addLayout(self.get_label_line("Indirizzo", self.cliente.get_indirizzo_cliente(), "in via"))
        v_lay_inf_sx.addLayout(self.get_label_line("Telefono", self.cliente.get_telefono_cliente(), "Telefono"))
        v_lay_inf_dx.addLayout(self.get_label_line("Email", self.cliente.get_email_cliente(), "E-mail"))
        v_lay_inf_sx.addStretch()
        v_lay_inf_sx.addWidget(btn_annulla)
        v_lay_inf_dx.addStretch()
        v_lay_inf_dx.addWidget(btn_modifica)
        h_lay_inf.addLayout(v_lay_inf_sx)
        h_lay_inf.addLayout(v_lay_inf_dx)

        self.v_layout.addLayout(h_lay_sup)
        self.v_layout.addLayout(h_lay_inf)

        self.setLayout(self.v_layout)
        self.setWindowTitle("Modifica Cliente")

    def get_label_line(self, tipo, campo, testo):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(testo))
        current_text_edit = QLineEdit(self)
        current_text_edit.setText(campo)
        layout.addWidget(current_text_edit)
        # popolo il dizionario
        self.info[tipo] = current_text_edit
        return layout

    def mod_cliente(self):
        # recupero i valori del dizionario
        nome = self.info["Nome"].text()
        cognome = self.info["Cognome"].text()
        cf = self.info["Codice Fiscale"].text()
        data_nascita = self.info["Data di nascita"].text()
        luogo_nascita = self.info["Luogo di nascita"].text()
        residenza = self.info["Residenza"].text()
        indirizzo = self.info["Indirizzo"].text()
        email = self.info["Email"].text()
        telefono = self.info["Telefono"].text()

        if nome == "" or cognome == "" or cf == "" or data_nascita == "" or luogo_nascita =="" or residenza =="" or \
                indirizzo == "" or email == "" or telefono == "":
            QMessageBox.critical(self, 'Errore', 'Per favore, inserisci tutte le informazioni richieste', QMessageBox.Ok, QMessageBox.Ok)
        else:
            if telefono.isnumeric() and len(telefono) == 10:
                if len(cf) == 16:
                    cliente1 = Cliente((nome + cognome).lower(), nome, cognome, cf, data_nascita, luogo_nascita, residenza,
                                       indirizzo, email, telefono)
                    abbonamento = self.cliente.get_abbonamento_cliente()
                    cliente1.aggiungi_abbonamento(abbonamento)
                    self.controller.rimuovi_dalla_lista(self.cl)
                    self.controller.aggiungi_cliente(cliente1)
                    self.callback()
                    self.close()
                else:
                    QMessageBox.critical(self, 'Errore',
                                         'Per favore inserisci un codice fiscale di telefono valido, 16 valori',
                                         QMessageBox.Ok, QMessageBox.Ok)
            else:
                QMessageBox.critical(self, 'Errore', 'Per favore inserisci un numero di telefono valido, 10 cifre',
                                     QMessageBox.Ok, QMessageBox.Ok)