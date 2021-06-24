from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QLabel, QLineEdit, QMessageBox, \
    QComboBox
from qtwidgets import PasswordEdit
from dipendente.controller.ControlloreDipendente import ControlloreDipendente
from dipendente.model.Dipendente import Dipendente


class VistaModificaDipendente(QWidget):
    def __init__(self, dipendente_selezionato, controller, callback):
        super(VistaModificaDipendente, self).__init__()
        self.dp = dipendente_selezionato
        self.dipendente = ControlloreDipendente(dipendente_selezionato)
        self.controller = controller
        self.callback = callback
        self.info = {}
        self.combo_abilitazione = QComboBox()

        self.v_layout = QVBoxLayout()

        self.get_form_entry(self.dipendente.get_nome_dipendente(), "Nome")
        self.get_form_entry(self.dipendente.get_cognome_dipendente(), "Cognome")
        self.get_form_entry(self.dipendente.get_data_dipendente(), "Data di nascita")
        self.get_form_entry(self.dipendente.get_luogo_dipendente(), "Luogo di nascita")
        self.get_form_entry(self.dipendente.get_cf_dipendente(), "Codice Fiscale")
        self.get_form_entry(self.dipendente.get_telefono_dipendente(), "Telefono")
        self.get_form_entry(self.dipendente.get_email_dipendente(), "Email")
        self.get_combo(["Collaboratore","Personal Trainer"])

        password =QLabel("Password")
        self.password = PasswordEdit()
        self.password.setText(self.dipendente.get_password_dipendente())
        self.v_layout.addWidget(password)
        self.v_layout.addWidget(self.password)
        self.info["Password"] = self.password

        self.v_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        btn_ok = QPushButton("OK")
        btn_ok.clicked.connect(self.modDipendente)
        self.v_layout.addWidget(btn_ok)

        self.setLayout(self.v_layout)
        self.setWindowTitle("Modifica Dipendente")

    def get_form_entry(self, campo, tipo):
        self.v_layout.addWidget(QLabel(tipo))
        current_text_edit = QLineEdit(self)
        current_text_edit.setText(campo)
        self.v_layout.addWidget(current_text_edit)
        self.info[tipo] = current_text_edit

    def get_combo(self, lista):
        self.v_layout.addWidget(QLabel("Abilitazione"))
        combo_model = QStandardItemModel(self.combo_abilitazione)
        combo_model.appendRow(QStandardItem(""))
        for item in lista:
            combo_model.appendRow(QStandardItem(item))
        self.combo_abilitazione.setModel(combo_model)
        self.combo_abilitazione.setCurrentText(self.dipendente.get_abilitazione_dipendente())
        self.v_layout.addWidget(self.combo_abilitazione)

    def modDipendente(self):
        nome = self.info["Nome"].text()
        cognome = self.info["Cognome"].text()
        data_nascita = self.info["Data di nascita"].text()
        luogo_nascita = self.info["Luogo di nascita"].text()
        cf = self.info["Codice Fiscale"].text()
        telefono = self.info["Telefono"].text()
        email = self.info["Email"].text()
        abilitazione = self.combo_abilitazione.currentText()
        password = self.info["Password"].text()
        if nome == "" or cognome == "" or data_nascita=="" or luogo_nascita==""  or cf == "" or telefono == "" or email == "" or abilitazione=="" or password=="":
             QMessageBox.critical(self, 'Errore', 'Per favore, inserisci tutte le informazioni richieste', QMessageBox.Ok,QMessageBox.Ok)
        else:
            dipendente = Dipendente(nome, cognome, data_nascita, luogo_nascita, cf, telefono, email, abilitazione, password)
            self.controller.rimuovi_dalla_lista(self.dp)
            self.controller.aggiungi_dipendente(dipendente)
            self.callback()
            self.close()