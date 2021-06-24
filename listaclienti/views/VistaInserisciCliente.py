from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QSpacerItem, QSizePolicy, QPushButton, QMessageBox, \
    QHBoxLayout

from cliente.model.Cliente import Cliente


class VistaInserisciCliente(QWidget):
    def __init__(self, controller, callback):
        super(VistaInserisciCliente, self).__init__()
        self.controller = controller
        self.callback = callback
        self.info = {}

        self.v_layout = QVBoxLayout()
        self.setFixedSize(600, 350)

        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(self.add_cliente)

        btn_annulla = QPushButton("Annulla")
        btn_annulla.clicked.connect(self.close)

        self.label_img = QLabel()
        self.label_img.setPixmap(QPixmap('listaclienti/data/utente.png'))

        h_lay_sup = QHBoxLayout()
        v_lay_sup_sx = QVBoxLayout()
        v_lay_sup_dx = QVBoxLayout()
        v_lay_sup_sx.addSpacerItem(QSpacerItem(40,40, QSizePolicy.Minimum, QSizePolicy.Minimum))
        v_lay_sup_sx.addLayout(self.get_label_line("Nome", "Nome","nome"))
        v_lay_sup_sx.addLayout(self.get_label_line("Cognome","Cognome","cognome"))
        v_lay_sup_sx.addLayout(self.get_label_line("Codice Fiscale", "Codice Fiscale","cod.fiscale"))
        v_lay_sup_dx.addWidget(self.label_img)
        h_lay_sup.addLayout(v_lay_sup_sx)
        h_lay_sup.addLayout(v_lay_sup_dx)

        h_lay_inf = QHBoxLayout()
        v_lay_inf_sx = QVBoxLayout()
        v_lay_inf_dx = QVBoxLayout()
        v_lay_inf_sx.addLayout(self.get_label_line("Nato a","Luogo di nascita","luogo di nascita"))
        v_lay_inf_dx.addLayout(self.get_label_line("il","Data di nascita","dd/mm/yyy"))
        v_lay_inf_sx.addLayout(self.get_label_line("Residente a ", "Residenza","residenza"))
        v_lay_inf_dx.addLayout(self.get_label_line("in via", "Indirizzo","via , n°"))
        v_lay_inf_sx.addLayout(self.get_label_line("Recapito telefonico", "Telefono","fisso/cellulare"))
        v_lay_inf_dx.addLayout(self.get_label_line("E-mail", "Email","email"))
        v_lay_inf_sx.addWidget(btn_annulla)
        v_lay_inf_dx.addWidget(btn_ok)
        h_lay_inf.addLayout(v_lay_inf_sx)
        h_lay_inf.addLayout(v_lay_inf_dx)

        self.v_layout.addLayout(h_lay_sup)
        self.v_layout.addLayout(h_lay_inf)

        self.setLayout(self.v_layout)
        self.setWindowTitle("Nuovo Cliente")

    def get_label_line(self, label, tipo, placeholder):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(label))
        current_text_edit = QLineEdit(self)
        current_text_edit.setPlaceholderText(placeholder)
        layout.addWidget(current_text_edit)
        self.info[tipo] = current_text_edit
        return layout

    def add_cliente(self):
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
            self.controller.aggiungiCliente(Cliente((nome+cognome).lower(), nome, cognome, cf, data_nascita, luogo_nascita, residenza,  indirizzo, email, telefono))
            self.callback()
            self.close()