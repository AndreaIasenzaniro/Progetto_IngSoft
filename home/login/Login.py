from PyQt5.QtWidgets import QWidget, QPushButton, QLabel, QLineEdit, QVBoxLayout, QMessageBox, QHBoxLayout
from PyQt5.QtCore import Qt
from qtwidgets import PasswordEdit

from amministratore.model.Amministratore import Amministratore
from home.views.VistaHome import VistaHome
from listadipendenti.controller.ControlloreListaDipendenti import *


class Login(QWidget):
    accesso_utente = None
    autorizzazione = None
    def __init__(self, parent = None):
        super(Login, self).__init__(parent)

        self.setWindowTitle('Login - Centro Polisportivo')
        self.setFixedSize(380,300)
        self.controller = ControlloreListaDipendenti()
        self.setStyleSheet("background-color: Azure;")

        # definisco un layout verticale per il login
        login_layout = QVBoxLayout()
        login_layout.setAlignment(Qt.AlignCenter)
        login_layout.setSpacing(25)
        # definisco un layout orizzontale per i pulsanti
        btn_layout = QHBoxLayout()

        # creazione campi inserimento username
        labelUsername = QLabel('<font size = "5"> <b> Username </b> </font>')
        self.username = QLineEdit()
        #self.username.setStyleSheet("background-color: #ffffff; font-size: 20px;")
        self.impostaGrandezzaMassima(self.username)
        self.username.setPlaceholderText('Inserisci username')
        # creazione campi inserimento password
        labelPassword = QLabel('<font size = "5"> <b> Password </b> </font>')
        self.password = PasswordEdit()
        #self.password.setStyleSheet("background-color: #ffffff; font-size: 20px;")
        self.impostaGrandezzaMassima(self.password)
        self.password.setPlaceholderText('Inserisci password')
        # creazione pulsante del login
        btn_login = QPushButton('Login')
        btn_login.setStyleSheet("background-color: #b0c4de; font-size: 15px; font-weight: bold;")
        self.impostaGrandezzaMassima(btn_login)
        btn_login.setShortcut("Return")
        btn_login.clicked.connect(self.check_credenziali)
        # creazione pulsante esci
        btn_esci = QPushButton('Esci')
        btn_esci.setStyleSheet("background-color: #b0c4de; font-size: 15px; font-weight: bold;")
        btn_esci.setShortcut("Esc")
        self.impostaGrandezzaMassima(btn_esci)
        btn_esci.clicked.connect(self.close)

        # aggiunta pulsanti al layout dei pulsanti
        btn_layout.addWidget(btn_login)
        btn_layout.addWidget(btn_esci)

        # aggiunta username al layout
        login_layout.addWidget(labelUsername)
        login_layout.addWidget(self.username)
        # aggiunta password al layout
        login_layout.addWidget(labelPassword)
        login_layout.addWidget(self.password)
        # aggiunta layout pulsanti al layout principale
        login_layout.addLayout(btn_layout)

        # setting del layout della finestra
        self.setLayout(login_layout)

    # funzione che esegue la verifica dell'utente e l'accesso all'area di competenza
    def check_credenziali(self):
        msg = QMessageBox()
        i=0
        if self.username.text() == Amministratore().get_username() and  self.password.text() == Amministratore().get_password():
            Login.autorizzazione_accesso="Amministratore"
            self.close()
            self.vistahome = VistaHome()
            self.vistahome.show()
        else:
            for dipendente in self.controller.get_lista_dipendenti():
                i += 1
                if self.password.text() == dipendente.password and self.username.text() == dipendente.id:
                    Login.autorizzazione_accesso = "Dipendente"
                    Login.accesso_utente = dipendente
                    # msg.setWindowTitle("Login corretto")
                    # msg.setText('Accesso effettuato correttamente. Buon lavoro!')
                    # msg.exec_()
                    self.close()
                    self.vistahome = VistaHome()
                    self.vistahome.show()
                    break

            if i == (len(self.controller.get_lista_dipendenti())) and (self.password.text() != dipendente.password or self.username.text() != dipendente.id):
                msg.setWindowTitle("Login errato")
                msg.setText('Password o Username errati. Riprova!')
                msg.exec_()
                # in caso di mancata autenticazione i campi di inserimento vengono resettati
                self.password.setText("")
                self.username.setText("")

    #imposta la grandezza massima di un "oggetto"
    def impostaGrandezzaMassima(self, oggetto):
        oggetto.setMinimumSize(25, 25)