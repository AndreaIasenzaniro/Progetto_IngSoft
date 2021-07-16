from PyQt5.QtCore import QDate, Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QLabel, QLineEdit, QMessageBox, \
    QComboBox, QCalendarWidget, QCheckBox, QHBoxLayout, QRadioButton
from datetime import  datetime
import time

from campo.model.Campo import Campo
from listamovimenti.controller.ControlloreListaMovimenti import ControlloreListaMovimenti
from listaprenotazioni.controller.ControlloreListaPrenotazioni import ControlloreListaPrenotazioni
from movimento.model.Movimento import Movimento
from prenotazione.model.Prenotazione import Prenotazione


class VistaInserisciPrenotazione(QWidget):
    def __init__(self, controller, callback):
        super(VistaInserisciPrenotazione, self).__init__()

        self.setFixedSize(300,600)
        
        self.controller = controller
        self.callback = callback
        self.info = {}
        self.c = ControlloreListaPrenotazioni()
        self.controlloreMov = ControlloreListaMovimenti()

        self.combo_ora = QComboBox()
        self.v_layout = QVBoxLayout()
        self.v_layout.addStretch()
        lbl_titolo = QLabel("<b>Nuova prenotazione</b>")
        font = lbl_titolo.font()
        font.setPointSize(20)
        lbl_titolo.setFont(font)
        lbl_titolo.setAlignment(Qt.AlignCenter)
        self.v_layout.addWidget(lbl_titolo)
        self.v_layout.addStretch()
        self.get_form_entry("Nome cliente")
        self.get_form_entry("Cognome cliente")
        self.get_form_entry("Documento")
        self.get_form_entry("Tipo campo")
        self.numero = QLabel("Numero Campo")
        self.v_layout.addWidget(self.numero)
        self.radio()

        self.data_label = QLabel("Data")
        self.v_layout.addWidget(self.data_label)
        self.btn_data = QPushButton("Inserisci data")
        self.btn_data.clicked.connect(self.visualizza_calendario)

        self.v_layout.addWidget(self.btn_data)

        self.lista_ore = ["10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00",
                          "14:30", "15:00","15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30",
                          "19:00", "19:30", "20:00", "20:30", "21:00", "21:30",]
        self.get_combo(self.lista_ore)

        self.v_layout.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Expanding))

        btn_ok = QPushButton("OK")
        btn_ok.setStyleSheet("background-color: #90ee90; font-size: 13px; font-weight: bold;")
        btn_ok.setShortcut("Return")
        btn_ok.clicked.connect(self.add_prenotazione)
        self.v_layout.addWidget(btn_ok)

        # creazione pulsante di annullamento dell'inserimento
        btn_annulla = QPushButton("Annulla")
        btn_annulla.setStyleSheet("background-color: #f08080; font-size: 13px; font-weight: bold;")
        btn_annulla.setShortcut("Esc")
        btn_annulla.clicked.connect(self.funz_esci)
        self.v_layout.addWidget(btn_annulla)
        self.v_layout.addStretch()

        self.setLayout(self.v_layout)
        self.setWindowTitle("Nuova Prenotazione")

    def get_form_entry(self, tipo):
        self.v_layout.addWidget(QLabel("<b>{}</b>".format(tipo)))
        current_text_edit = QLineEdit(self)
        font = current_text_edit.font()
        font.setPointSize(15)
        current_text_edit.setFont(font)
        self.v_layout.addWidget(current_text_edit)
        if tipo =="Tipo campo":
            from home.views.VistaHome import VistaHome
            current_text_edit.setText(VistaHome.selezione_campo)
            current_text_edit.setReadOnly(True)
        self.info[tipo] = current_text_edit

    def get_combo(self, lista):
        self.v_layout.addWidget(QLabel("Ora inizio"))
        combo_model = QStandardItemModel(self.combo_ora)
        combo_model.appendRow(QStandardItem(""))
        for item in lista:
            combo_model.appendRow(QStandardItem(item))
        self.combo_ora.setModel(combo_model)
        self.v_layout.addWidget(self.combo_ora)

    def radio(self):
        self.h_layout =QHBoxLayout()
        self.radiobuttons1 = QRadioButton("1")
        self.radiobuttons1.setChecked(False)
        self.h_layout.addWidget(self.radiobuttons1)

        self.radiobuttons2 = QRadioButton("2")
        self.radiobuttons2.setChecked(False)
        self.h_layout.addWidget(self.radiobuttons2)

        self.v_layout.addLayout(self.h_layout)

    def add_prenotazione(self):
        from calendario.Calendario import Calendario
        Calendario.vista_prenotazione = False
        nome = self.info["Nome cliente"].text()
        cognome = self.info["Cognome cliente"].text()
        documento = self.info["Documento"].text()
        tipo_campo = self.info["Tipo campo"].text()
        ora_inizio = self.combo_ora.currentText()
        if self.radiobuttons1.isChecked():
            numero_campo = self.radiobuttons1.text()
        elif self.radiobuttons2.isChecked():
            numero_campo=self.radiobuttons2.text()
        else:
            numero_campo=""

        data_unix = self.data_selezionata()
        print("ddddddddddddddddddd {}".format(self.data_selezionata()))
        '''
        try:
            data_formattata = datetime.strptime(data, '%d/%m/%Y')
            data2_timestamp = datetime.timestamp(data_formattata)
        except:
            QMessageBox.critical(self, 'Errore', 'Errore, hai inserito un giorno già passato o una domenica (la domenica il centro è chiuso',
                                 QMessageBox.Ok, QMessageBox.Ok)'''
        today = datetime.today()
        today_formattato = today.strftime("%d/%m/%Y")
        today_formattato_per_unix= datetime.strptime(today_formattato,'%d/%m/%Y')
        today_unix = datetime.timestamp(today_formattato_per_unix)

        orario_today = str(today.hour) + ":" + str(today.minute)

        if nome == "" or cognome == "" or documento == "" or ora_inizio=="" or numero_campo=="" or data_unix is None:
            QMessageBox.critical(self, 'Errore', 'Per favore, inserisci tutte le informazioni richieste', QMessageBox.Ok, QMessageBox.Ok)
        elif data_unix=="Errore":
            QMessageBox.critical(self, 'Errore', 'Hai inserito una data passata o una domenica',
                                 QMessageBox.Ok, QMessageBox.Ok)
        elif data_unix == today_unix:
            if ora_inizio < orario_today:
                QMessageBox.critical(self, 'Errore', 'Errore hai inserito la data di oggi con un orario già passato',
                                     QMessageBox.Ok, QMessageBox.Ok)
            else:
                print("Nessun campo d'inserimento vuoto")
                self.campo = Campo(tipo_campo, numero_campo)
                print("Campo creato")
                self.prenotazione = Prenotazione(nome, cognome, documento, self.campo, self.data, ora_inizio)
                print("Prenotazione creata")
                if not self.c.get_lista_prenotazioni():
                    print("La lista è vuota")
                    self.campo.prenota()
                    self.controller.aggiungi_prenotazione(self.prenotazione)
                    self.aggiungi_movimento()
                    self.callback()
                    self.controller.save_data()
                    self.close()
                else:
                    for prenotazione_esistente in self.c.get_lista_prenotazioni():
                        print("Scorro la lista")
                        if self.confronta(prenotazione_esistente.data, self.prenotazione.data):
                            if self.confronta(prenotazione_esistente.campo.tipo, self.prenotazione.campo.tipo):
                                if self.confronta(prenotazione_esistente.campo.numero, self.prenotazione.campo.numero):
                                    if prenotazione_esistente.ora_inizio <= self.prenotazione.ora_inizio \
                                            and self.prenotazione.ora_inizio < prenotazione_esistente.ora_fine:
                                        print("Errore coincidenza ora inizio")
                                        QMessageBox.critical(self, 'Errore',
                                                             "Impossibile effettuare la prenotazione, poichè l'inizio dell'evento è compreso in un altro evento già prenotato",
                                                             QMessageBox.Ok, QMessageBox.Ok)
                                        break
                                    elif self.prenotazione.ora_fine > prenotazione_esistente.ora_inizio \
                                            and self.prenotazione.ora_fine < prenotazione_esistente.ora_fine:
                                        print("Errore coincidenza ora fine")
                                        QMessageBox.critical(self, 'Errore',
                                                             "Impossibile effettuare la prenotazione, poichè la fine dell'evento è compreso in un altro evento già prenotato",
                                                             QMessageBox.Ok, QMessageBox.Ok)
                                        break
                                    else:
                                        if self.verifica_ultimo_elemento_lista(prenotazione_esistente):
                                            print(prenotazione_esistente.nome + prenotazione_esistente.cognome)
                                            self.crea_parametri()
                                            print("Creato al passo 1")
                                        else:
                                            pass
                                else:
                                    if self.verifica_ultimo_elemento_lista(prenotazione_esistente):
                                        print(prenotazione_esistente.nome + prenotazione_esistente.cognome)
                                        self.crea_parametri()
                                        print("Creato al passo 2")
                                    else:
                                        pass
                            else:
                                if self.verifica_ultimo_elemento_lista(prenotazione_esistente):
                                    print(prenotazione_esistente.nome + prenotazione_esistente.cognome)
                                    self.crea_parametri()
                                    print("Creato al passo 3")
                                else:
                                    pass
                        else:
                            if self.verifica_ultimo_elemento_lista(prenotazione_esistente):
                                print(prenotazione_esistente.nome + prenotazione_esistente.cognome)
                                self.crea_parametri()
                                print("Creato al passo 4")
                            else:
                                pass
        elif data_unix != today_unix:
            print("Nessun campo d'inserimento vuoto")
            self.campo=Campo(tipo_campo, numero_campo)
            print("Campo creato")
            self.prenotazione = Prenotazione(nome, cognome, documento, self.campo, self.data, ora_inizio)
            print("Prenotazione creata")
            if not self.c.get_lista_prenotazioni():
                print("La lista è vuota")
                self.campo.prenota()
                self.controller.aggiungi_prenotazione(self.prenotazione)
                self.aggiungi_movimento()
                self.callback()
                self.controller.save_data()
                self.close()
            else:
                for prenotazione_esistente in self.c.get_lista_prenotazioni():
                    print("Scorro la lista")
                    if self.confronta(prenotazione_esistente.data, self.prenotazione.data):
                        if self.confronta(prenotazione_esistente.campo.tipo, self.prenotazione.campo.tipo):
                            if self.confronta(prenotazione_esistente.campo.numero, self.prenotazione.campo.numero):
                                if prenotazione_esistente.ora_inizio <= self.prenotazione.ora_inizio \
                                    and self.prenotazione.ora_inizio < prenotazione_esistente.ora_fine:
                                    print("Errore coincidenza ora inizio")
                                    QMessageBox.critical(self, 'Errore', "Impossibile effettuare la prenotazione, poichè l'inizio dell'evento è compreso in un altro evento già prenotato",QMessageBox.Ok, QMessageBox.Ok)
                                    break
                                elif self.prenotazione.ora_fine > prenotazione_esistente.ora_inizio \
                                    and self.prenotazione.ora_fine < prenotazione_esistente.ora_fine:
                                    print("Errore coincidenza ora fine")
                                    QMessageBox.critical(self, 'Errore',"Impossibile effettuare la prenotazione, poichè la fine dell'evento è compreso in un altro evento già prenotato",QMessageBox.Ok, QMessageBox.Ok)
                                    break
                                else:
                                    if self.verifica_ultimo_elemento_lista(prenotazione_esistente):
                                        print(prenotazione_esistente.nome + prenotazione_esistente.cognome)
                                        self.crea_parametri()
                                        print("Creato al passo 1")
                                    else:
                                        pass
                            else:
                                if self.verifica_ultimo_elemento_lista(prenotazione_esistente):
                                    print(prenotazione_esistente.nome + prenotazione_esistente.cognome)
                                    self.crea_parametri()
                                    print("Creato al passo 2")
                                else:
                                    pass
                        else:
                            if self.verifica_ultimo_elemento_lista(prenotazione_esistente):
                                print(prenotazione_esistente.nome + prenotazione_esistente.cognome)
                                self.crea_parametri()
                                print("Creato al passo 3")
                            else:
                                pass
                    else:
                        if self.verifica_ultimo_elemento_lista(prenotazione_esistente):
                            print(prenotazione_esistente.nome + prenotazione_esistente.cognome)
                            self.crea_parametri()
                            print("Creato al passo 4")
                        else:
                            pass


    def aggiungi_data(self):
        self.data_da_calendario = QCalendarWidget()
        self.data_da_calendario.setGridVisible(True)
        self.data_da_calendario.show()

    def data_selezionata(self):
        #vedere se bisogna fare queste successive 4 righe anche in VistaAbbonamento e VistaCertificato, perche il .today
        #ritorna anche i secondi nel timestamp
        oggi = datetime.today()
        oggi_formattato = oggi.strftime("%d/%m/%Y")
        oggi_formattato_per_unix = datetime.strptime(oggi_formattato, '%d/%m/%Y')
        oggi_unix = datetime.timestamp(oggi_formattato_per_unix)
        print("Oggi: " + str(oggi_unix))
        try:
            data_selezionata = self.calendario.selectedDate()
            self.data = "{}/{}/{}".format(data_selezionata.day(), data_selezionata.month(), data_selezionata.year())
            data_selezionata_formattata = datetime.strptime(self.data, '%d/%m/%Y')
            data_timestamp = datetime.timestamp(data_selezionata_formattata)
            print("Data selezionata: " + str(data_timestamp))
            if oggi_unix <= data_timestamp and data_selezionata.dayOfWeek() != 7:
                self.calendario.close()
                return data_timestamp
            elif data_timestamp is None:
                return None
            elif data_timestamp < oggi_unix:
                return("Errore")
        except:
            pass

    def visualizza_calendario(self):
        self.window = QWidget()
        self.v1_layout = QVBoxLayout()
        self.calendario = QCalendarWidget()
        self.calendario.setGridVisible(True)
        self.v1_layout.addWidget(self.calendario)
        self.btn_conferma = QPushButton("Conferma")
        self.btn_conferma.clicked.connect(self.window.close)
        self.v1_layout.addWidget(self.btn_conferma)
        self.window.setLayout(self.v1_layout)
        self.window.show()

    def crea_parametri(self):
        self.campo.prenota()
        self.controller.aggiungi_prenotazione(self.prenotazione)
        self.aggiungi_movimento()
        self.callback()
        self.controller.save_data()
        self.close()

    def confronta(self,prenotazione_esistente, nuova_prenotazione):
        if prenotazione_esistente == nuova_prenotazione:
            return True
        else:
            return None

    def verifica_ultimo_elemento_lista(self, prenotazione_corrente):
        if prenotazione_corrente == self.c.get_prenotazione_by_index(len(self.c.get_lista_prenotazioni()) - 1):
            return True
        else:
            return None

    def aggiungi_movimento(self):
        self.movimento = Movimento(self.data, "Prenotazione campo da " + self.info["Tipo campo"].text() + " - ID prenotazione: " + str(self.prenotazione.id),"Incasso", float(self.prenotazione.prezzi_campi()))
        self.movimento.isEntrata = True
        print("Stiamo aggiungendo")
        self.controlloreMov.aggiungi_movimento(self.movimento)
        print("Abbiamo aggiunto")
        self.controlloreMov.save_data()
        print("Abbiamo salvato")

    def funz_esci(self):
        self.close()
        from calendario.Calendario import Calendario
        Calendario.vista_prenotazione = False