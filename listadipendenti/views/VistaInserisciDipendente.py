from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QSpacerItem, QSizePolicy, QPushButton, QMessageBox, \
    QComboBox
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

        self.get_form_entry("Nome")
        self.get_form_entry("Cognome")
        self.get_form_entry("Data di nascita")
        self.get_form_entry("Luogo di nascita")
        self.get_form_entry("Codice Fiscale")
        self.get_form_entry("Telefono")
        self.get_form_entry("Email")
        self.get_combo(["Collaboratore","Personal Trainer"])

        password = QLabel("Password")
        self.password = PasswordEdit()
        self.password.setPlaceholderText('Inserisci password')
        self.v_layout.addWidget(password)
        self.v_layout.addWidget(self.password)
        self.info["Password"] = self.password

        self.v_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        btn_ok = QPushButton("OK")
        btn_ok.setStyleSheet("background-color: #90ee90; font-size: 15px; font-weight: bold;")
        btn_ok.setShortcut("Return")
        btn_ok.clicked.connect(self.add_dipendente)
        self.v_layout.addWidget(btn_ok)

        # creazione pulsante di annullamento dell'inserimento
        btn_annulla = QPushButton("Annulla")
        btn_annulla.setStyleSheet("background-color: #f08080; font-size: 15px; font-weight: bold;")
        btn_annulla.setShortcut("Esc")
        btn_annulla.clicked.connect(self.close)
        self.v_layout.addWidget(btn_annulla)

        self.setLayout(self.v_layout)
        self.setWindowTitle("Nuovo Dipendente")

    def get_form_entry(self, tipo):
        self.v_layout.addWidget(QLabel(tipo))
        current_text_edit = QLineEdit(self)
        self.v_layout.addWidget(current_text_edit)
        self.info[tipo] = current_text_edit

    def get_combo(self, lista):
        self.v_layout.addWidget(QLabel("Abilitazione"))
        combo_model = QStandardItemModel(self.combo_abilitazione)
        combo_model.appendRow(QStandardItem(""))
        for item in lista:
            combo_model.appendRow(QStandardItem(item))
        self.combo_abilitazione.setModel(combo_model)
        self.v_layout.addWidget(self.combo_abilitazione)

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