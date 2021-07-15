from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QSpacerItem, QSizePolicy, QPushButton, QMessageBox, \
    QComboBox, QHBoxLayout
from qtwidgets import PasswordEdit

from cliente.model.Cliente import Cliente
from dipendente.model.Dipendente import Dipendente

class VistaInserisciDipendente(QWidget):
    def __init__(self, controller, callback):
        super(VistaInserisciDipendente, self).__init__()
        self.controller = controller
        self.callback = callback
        self.info = {}
        self.combo_abilitazione = QComboBox()

        self.v_layout = QVBoxLayout()
        self.setFixedSize(650, 470)

        btn_ok = QPushButton("OK")
        btn_ok.setStyleSheet("background-color: #90ee90; font-size: 13px; font-weight: bold;")
        btn_ok.setShortcut("Return")
        btn_ok.clicked.connect(self.add_dipendente)
        #self.v_layout.addWidget(btn_ok)
        # creazione pulsante di annullamento dell'inserimento
        btn_annulla = QPushButton("Annulla")
        btn_annulla.setStyleSheet("background-color: #f08080; font-size: 13px; font-weight: bold;")
        btn_annulla.setShortcut("Esc")
        btn_annulla.clicked.connect(self.close)
        #self.v_layout.addWidget(btn_annulla)

        self.label_img = QLabel()
        self.label_img.setPixmap(QPixmap('listadipendenti/data/utente.png'))
        # layout superiore
        h_lay_sup = QHBoxLayout()
        v_lay_sup_sx = QVBoxLayout()
        v_lay_sup_dx = QVBoxLayout()
        v_lay_sup_sx.addStretch()
        v_lay_sup_sx.addLayout(self.get_label_line("Nome", "Nome", "nome"))
        v_lay_sup_sx.addLayout(self.get_label_line("Cognome", "Cognome", "cognome"))
        v_lay_sup_sx.addLayout(self.get_label_line("Codice Fiscale", "Codice Fiscale", "cod.fiscale"))
        v_lay_sup_sx.addStretch()
        v_lay_sup_dx.addWidget(self.label_img)
        h_lay_sup.addLayout(v_lay_sup_sx)
        h_lay_sup.addLayout(v_lay_sup_dx)
        # layout centrale
        h_lay_cent = QHBoxLayout()
        v_lay_cent_sx = QVBoxLayout()
        v_lay_cent_dx = QVBoxLayout()
        v_lay_cent_sx.addLayout(self.get_label_line("Nato a", "Luogo di nascita", "luogo di nascita"))
        v_lay_cent_dx.addLayout(self.get_label_line("il", "Data di nascita", "dd/mm/yyy"))
        v_lay_cent_sx.addLayout(self.get_label_line("Residente a ", "Residenza", "residenza"))
        v_lay_cent_dx.addLayout(self.get_label_line("in via", "Indirizzo", "via , n°"))
        v_lay_cent_sx.addLayout(self.get_label_line("Recapito telefonico", "Telefono", "fisso/cellulare"))
        v_lay_cent_dx.addLayout(self.get_label_line("E-mail", "Email", "email"))
        h_lay_cent.addLayout(v_lay_cent_sx)
        h_lay_cent.addLayout(v_lay_cent_dx)
        # layout inferiore
        v_lay_inf = QVBoxLayout()
        h_lay_inf = QHBoxLayout()
        h_lay_inf_btn = QHBoxLayout()
        password = QLabel("<b>Password</b>")
        self.password = PasswordEdit()
        self.password.setPlaceholderText('Inserisci password')
        h_lay_inf.addWidget(password)
        h_lay_inf.addWidget(self.password)
        self.info["Password"] = self.password
        #h_lay_inf_btn.addStretch()
        h_lay_inf_btn.addWidget(btn_annulla)
        #h_lay_inf_btn.addStretch()
        h_lay_inf_btn.addWidget(btn_ok)
        v_lay_inf.addLayout(h_lay_inf)
        v_lay_inf.addStretch()
        v_lay_inf.addLayout(h_lay_inf_btn)

        self.v_layout.addLayout(h_lay_sup)
        self.v_layout.addLayout(self.get_combo(["Collaboratore", "Personal Trainer"]))
        #self.get_combo(["Collaboratore", "Personal Trainer"])
        self.v_layout.addLayout(h_lay_cent)
        self.v_layout.addLayout(v_lay_inf)

        self.setLayout(self.v_layout)
        self.setWindowTitle("Nuovo Dipendente")

    def get_label_line(self, label, tipo, placeholder):
        layout = QHBoxLayout()
        layout.addWidget(QLabel("<b>{}</b>".format(label)))
        current_text_edit = QLineEdit(self)
        current_text_edit.setPlaceholderText(placeholder)
        #current_text_edit.setGeometry(70,30,70,30)
        layout.addWidget(current_text_edit)
        self.info[tipo] = current_text_edit
        return layout

    def get_combo(self, lista):
        v_lay = QVBoxLayout()
        v_lay.addWidget(QLabel("<b>Abilitazione</b>"))
        combo_model = QStandardItemModel(self.combo_abilitazione)
        combo_model.appendRow(QStandardItem(""))
        for item in lista:
            combo_model.appendRow(QStandardItem(item))
        self.combo_abilitazione.setModel(combo_model)
        v_lay.addWidget(self.combo_abilitazione)
        #h_lay.addItem(QSpacerItem(300,10,QSizePolicy.Minimum,QSizePolicy.Minimum))
        return v_lay

    def add_dipendente(self):
        nome = self.info["Nome"].text()
        cognome = self.info["Cognome"].text()
        datanascita = self.info["Data di nascita"].text()
        luogonascita = self.info["Luogo di nascita"].text()
        cf = self.info["Codice Fiscale"].text()
        telefono = self.info["Telefono"].text()
        email = self.info["Email"].text()
        abilitazione = self.combo_abilitazione.currentText()
        password = self.info["Password"].text()

        if nome == "" or cognome == "" or cf == "" or datanascita == "" or luogonascita == "" or cf == "" \
                or telefono == "" or email == "" or abilitazione == "" or password == "":
            QMessageBox.critical(self, 'Errore', 'Per favore, inserisci tutte le informazioni richieste', QMessageBox.Ok, QMessageBox.Ok)
        else:
            self.controller.aggiungi_dipendente(Dipendente(nome, cognome, datanascita, luogonascita, cf, telefono, email, abilitazione, password))
            self.callback()
            self.close()