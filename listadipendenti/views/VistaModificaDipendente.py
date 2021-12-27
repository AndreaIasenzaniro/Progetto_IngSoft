from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QLabel, QLineEdit, QMessageBox, \
    QComboBox, QHBoxLayout
from qtwidgets import PasswordEdit
from dipendente.controller.ControlloreDipendente import ControlloreDipendente
from dipendente.model.Dipendente import Dipendente


class VistaModificaDipendente(QWidget):
    def __init__(self, dipendente_selezionato, controller, callback):
        super(VistaModificaDipendente, self).__init__()

        self.dp = dipendente_selezionato
        # passo alla classe il dipendente che seleziono per avere le sue informazioni
        self.dipendente = ControlloreDipendente(dipendente_selezionato)
        self.controller = controller
        self.callback = callback
        self.info = {}
        self.combo_abilitazione = QComboBox()

        # layout di modifica dei dati del dipendente
        self.v_layout = QVBoxLayout()
        self.setFixedSize(650, 470)

        # pulsante di conferma della modifica
        btn_modifica = QPushButton("Modifica")
        btn_modifica.setStyleSheet("background-color: #90ee90; font-size: 13px; font-weight: bold;")
        btn_modifica.setShortcut("Return")
        btn_modifica.clicked.connect(self.mod_dipendente)
        # pulsante di annullamento delle modifica
        btn_annulla = QPushButton("Annulla")
        btn_annulla.setStyleSheet("background-color: #f08080; font-size: 13px; font-weight: bold;")
        btn_annulla.setShortcut("Esc")
        btn_annulla.clicked.connect(self.close)

        self.label_img = QLabel()
        self.label_img.setPixmap(QPixmap('listadipendenti/data/utente.png'))

        # layout superiore
        h_lay_sup = QHBoxLayout()
        v_lay_sup_sx = QVBoxLayout()
        v_lay_sup_dx = QVBoxLayout()
        v_lay_sup_sx.addStretch()
        v_lay_sup_sx.addLayout(self.get_form_entry(self.dipendente.get_nome_dipendente(), "Nome"))
        v_lay_sup_sx.addLayout(self.get_form_entry(self.dipendente.get_cognome_dipendente(), "Cognome"))
        v_lay_sup_sx.addLayout(self.get_form_entry(self.dipendente.get_cf_dipendente(), "Codice Fiscale"))
        v_lay_sup_sx.addStretch()
        v_lay_sup_dx.addWidget(self.label_img)
        h_lay_sup.addLayout(v_lay_sup_sx)
        h_lay_sup.addLayout(v_lay_sup_dx)
        # layout centrale
        h_lay_cent = QHBoxLayout()
        v_lay_cent_sx = QVBoxLayout()
        v_lay_cent_dx = QVBoxLayout()
        v_lay_cent_sx.addLayout(self.get_form_entry(self.dipendente.get_luogo_dipendente(), "Luogo di nascita"))
        v_lay_cent_dx.addLayout(self.get_form_entry(self.dipendente.get_data_dipendente(), "Data di nascita"))
        v_lay_cent_sx.addLayout(self.get_form_entry(self.dipendente.get_residenza_dipendente(), "Residenza"))
        v_lay_cent_dx.addLayout(self.get_form_entry(self.dipendente.get_indirizzo_dipendente(), "Indirizzo"))
        v_lay_cent_sx.addLayout(self.get_form_entry(self.dipendente.get_telefono_dipendente(), "Telefono"))
        v_lay_cent_dx.addLayout(self.get_form_entry(self.dipendente.get_email_dipendente(), "Email"))
        h_lay_cent.addLayout(v_lay_cent_sx)
        h_lay_cent.addLayout(v_lay_cent_dx)
        # layout inferiore
        v_lay_inf = QVBoxLayout()
        h_lay_inf = QHBoxLayout()
        h_lay_inf_btn = QHBoxLayout()

        password = QLabel("<b>Password</b>")
        self.password = PasswordEdit()
        self.password.setText(self.dipendente.get_password_dipendente())
        h_lay_inf.addWidget(password)
        h_lay_inf.addWidget(self.password)
        self.info["Password"] = self.password

        h_lay_inf_btn.addWidget(btn_annulla)
        h_lay_inf_btn.addWidget(btn_modifica)
        v_lay_inf.addLayout(h_lay_inf)
        v_lay_inf.addStretch()
        v_lay_inf.addLayout(h_lay_inf_btn)

        self.v_layout.addLayout(h_lay_sup)
        self.v_layout.addLayout(self.get_combo(["Collaboratore", "Personal Trainer"]))

        self.v_layout.addLayout(h_lay_cent)
        self.v_layout.addLayout(v_lay_inf)

        self.setLayout(self.v_layout)
        self.setWindowTitle("Modifica Dipendente")

    # ritorna layout con i campi da moficiare con relative etichette
    def get_form_entry(self, campo, tipo):
        h_lay = QHBoxLayout()
        h_lay.addWidget(QLabel("<b>{}</b>".format(tipo)))
        current_text_edit = QLineEdit(self)
        current_text_edit.setText(campo)
        h_lay.addWidget(current_text_edit)
        self.info[tipo] = current_text_edit
        return h_lay

    # ottengo i dati della combo per l'abilitazione
    def get_combo(self, lista):
        v_lay = QVBoxLayout()
        v_lay.addWidget(QLabel("<b>Abilitazione</b>"))
        combo_model = QStandardItemModel(self.combo_abilitazione)
        combo_model.appendRow(QStandardItem(""))
        for item in lista:
            combo_model.appendRow(QStandardItem(item))
        self.combo_abilitazione.setModel(combo_model)
        # setto il valore della combo con l'abilitazione attuale del dipendente
        self.combo_abilitazione.setCurrentText(self.dipendente.get_abilitazione_dipendente())
        v_lay.addWidget(self.combo_abilitazione)
        return v_lay

    def mod_dipendente(self):
        # recupero i valori del dizionario
        nome = self.info["Nome"].text()
        cognome = self.info["Cognome"].text()
        data_nascita = self.info["Data di nascita"].text()
        luogo_nascita = self.info["Luogo di nascita"].text()
        residenza = self.info["Residenza"].text()
        indirizzo = self.info["Indirizzo"].text()
        cf = self.info["Codice Fiscale"].text()
        telefono = self.info["Telefono"].text()
        email = self.info["Email"].text()
        abilitazione = self.combo_abilitazione.currentText()
        password = self.info["Password"].text()
        # effettuo i controlli per i dati immessi come per l'inserimento di un nuovo cliente
        if nome == "" or cognome == "" or data_nascita=="" or luogo_nascita==""  or cf == "" or telefono == "" or email == "" or abilitazione=="" or password=="":
             QMessageBox.critical(self, 'Errore', 'Per favore, inserisci tutte le informazioni richieste', QMessageBox.Ok,QMessageBox.Ok)
        else:
            if telefono.isnumeric() and len(telefono) == 10:
                if len(cf) == 16:
                    dipendente = Dipendente(nome, cognome, data_nascita, luogo_nascita, residenza, indirizzo, cf, telefono,
                                            email, abilitazione, password)
                    self.controller.rimuovi_dalla_lista(self.dp)
                    self.controller.aggiungi_dipendente(dipendente)
                    self.callback()
                    self.close()
                else:
                    QMessageBox.critical(self, 'Errore', 'Per favore inserisci un codice fiscale di telefono valido, 16 valori',
                                         QMessageBox.Ok, QMessageBox.Ok)
            else:
                QMessageBox.critical(self, 'Errore', 'Per favore inserisci un numero di telefono valido, 10 cifre', QMessageBox.Ok, QMessageBox.Ok)
