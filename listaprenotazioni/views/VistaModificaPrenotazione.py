from PyQt5.QtCore import QDate
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSpacerItem, QSizePolicy, QPushButton, QLabel, QLineEdit, QMessageBox, \
    QComboBox, QHBoxLayout, QRadioButton, QCalendarWidget


from campo.model.Campo import Campo
from listaprenotazioni.controller.ControlloreListaPrenotazioni import ControlloreListaPrenotazioni
from prenotazione.controller.ControllorePrenotazione import ControllorePrenotazione
from datetime import  datetime
from prenotazione.model.Prenotazione import Prenotazione

class VistaModificaPrenotazione(QWidget):
    def __init__(self, prenotazione_selezionata, controller, callback):
        super(VistaModificaPrenotazione, self).__init__()
        self.p = prenotazione_selezionata
        self.prenotazione_sel = ControllorePrenotazione(prenotazione_selezionata)
        self.controller = controller
        self.callback = callback
        self.info = {}
        self.info = {}
        self.c = ControlloreListaPrenotazioni()

        self.combo_ora = QComboBox()

        self.v_layout = QVBoxLayout()

        self.get_form_entry(self.prenotazione_sel.get_nome(),"Nome cliente")
        self.get_form_entry(self.prenotazione_sel.get_cognome(),"Cognome cliente")
        self.get_form_entry(self.prenotazione_sel.get_documento(),"Documento")
        self.get_form_entry(self.prenotazione_sel.get_campo_tipo(),"Tipo campo")


        self.numero = QLabel("Numero Campo")
        self.v_layout.addWidget(self.numero)
        self.radio()

        print(QDate.currentDate())

        self.data_label = QLabel("Data")
        self.v_layout.addWidget(self.data_label)
        self.btn_data = QPushButton("Inserisci data")
        self.btn_data.clicked.connect(self.visualizza_calendario)

        self.v_layout.addWidget(self.btn_data)

        self.lista_ore = ["10:00", "10:30", "11:00", "11:30", "12:00", "12:30", "13:00", "13:30", "14:00",
                          "14:30", "15:00", "15:30", "16:00", "16:30", "17:00", "17:30", "18:00", "18:30",
                          "19:00", "19:30", "20:00", "20:30", "21:00", "21:30", ]
        self.get_combo(self.lista_ore)

        self.v_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))

        btn_ok = QPushButton("OK")
        btn_ok.setStyleSheet("background-color: #90ee90; font-size: 15px; font-weight: bold;")
        btn_ok.setShortcut("Return")
        btn_ok.clicked.connect(self.add_prenotazione)
        self.v_layout.addWidget(btn_ok)

        # creazione pulsante di annullamento dell'inserimento
        btn_annulla = QPushButton("Annulla")
        btn_annulla.setStyleSheet("background-color: #f08080; font-size: 15px; font-weight: bold;")
        btn_annulla.setShortcut("Esc")
        btn_annulla.clicked.connect(self.close)
        self.v_layout.addWidget(btn_annulla)

        self.setLayout(self.v_layout)
        self.setWindowTitle("Nuova Prenotazione")

    def get_form_entry(self, campo, tipo):
        self.v_layout.addWidget(QLabel(tipo))
        current_text_edit = QLineEdit(self)
        current_text_edit.setText(campo)
        self.v_layout.addWidget(current_text_edit)
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



        self.data_unix = self.data_selezionata()

        if self.data_unix is None:
            self.assegno_data = self.prenotazione_sel.get_data_prenotazione()
            print(self.assegno_data + "ASSEGNO DATA")
            self.data_form = datetime.strptime(self.assegno_data, '%d/%m/%Y')
            self.data_times = datetime.timestamp(self.data_form)
            self.data_unix = self.data_times
            print(str(self.data_unix) + "DATA UNIX")
        else:
            self.assegno_data = self.data



        today = datetime.today()
        today_formattato = today.strftime("%d/%m/%Y")
        today_formattato_per_unix= datetime.strptime(today_formattato,'%d/%m/%Y')
        today_unix = datetime.timestamp(today_formattato_per_unix)

        orario_today = str(today.hour) + ":" + str(today.minute)

        if nome == "" or cognome == "" or documento == "" or ora_inizio=="" or numero_campo=="" or self.data_unix is None:
            QMessageBox.critical(self, 'Errore', 'Per favore, inserisci tutte le informazioni richieste', QMessageBox.Ok, QMessageBox.Ok)
        elif self.data_unix=="Errore":
            QMessageBox.critical(self, 'Errore', 'Hai inserito una data passata o una domenica',
                                 QMessageBox.Ok, QMessageBox.Ok)
        elif self.data_unix == today_unix:
            if ora_inizio < orario_today:
                QMessageBox.critical(self, 'Errore', 'Errore hai inserito la data di oggi con un orario già passato',
                                     QMessageBox.Ok, QMessageBox.Ok)
            else:
                print("Nessun campo d'inserimento vuoto")
                self.campo = Campo(tipo_campo, numero_campo)
                print("Campo creato")
                self.prenotazione = Prenotazione(nome, cognome, documento, self.campo, self.assegno_data, ora_inizio)
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
        elif self.data_unix != today_unix:
            print("Nessun campo d'inserimento vuoto")
            self.campo=Campo(tipo_campo, numero_campo)
            print("Campo creato")
            self.prenotazione = Prenotazione(nome, cognome, documento, self.campo, self.assegno_data, ora_inizio)
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
        self.controller.rimuovi_dalla_lista(self.p)
        self.controller.save_data()
        self.controller.aggiungi_prenotazione(self.prenotazione)
        self.controller.save_data()
        self.callback()
        from calendario.Calendario import Calendario
        self.close()
        self.controller.save_data()
        self.mostra_calendario = Calendario()
        return self.mostra_calendario.show()

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

