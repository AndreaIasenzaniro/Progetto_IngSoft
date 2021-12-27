from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy, \
    QMessageBox

from abbonamento.views.VistaAbbonamento import VistaAbbonamento
from certificato.views.VistaCertificato import VistaCertificato
from cliente.controller.ControlloreCliente import ControlloreCliente
from listaclienti.controller.ControlloreListaClienti import ControlloreListaClienti


class VistaCliente(QWidget):
    def __init__(self, cliente, elimina_cliente, elimina_callback, parent=None):
        super(VistaCliente, self).__init__(parent)

        # controllore del cliente che passo con selezione
        self.controller = ControlloreCliente(cliente)
        # funzioni di eliminazione passata alla Vista
        self.elimina_cliente = elimina_cliente
        self.elimina_callback = elimina_callback
        self.v_layout = QVBoxLayout()

        # immagine profilo cliente
        self.label_img = QLabel()
        self.label_img.setPixmap(QPixmap('listaclienti/data/utente.png'))
        self.setWindowTitle("Scheda cliente: " + self.controller.get_nome_cliente() + " " + self.controller.get_cognome_cliente())

        # nome cliente visualizzato in grande
        label_nome = QLabel(self.controller.get_nome_cliente() + " " + self.controller.get_cognome_cliente())
        font_nome = label_nome.font()
        font_nome.setPointSize(20)
        label_nome.setFont(font_nome)

        # layout superiore
        h_lay_sup = QHBoxLayout()
        v_lay_sup_sx = QVBoxLayout()
        v_lay_sup_dx = QVBoxLayout()
        v_lay_sup_sx.addWidget(self.label_img)
        v_lay_sup_dx.addStretch()
        v_lay_sup_dx.addWidget(label_nome)
        v_lay_sup_dx.addItem(QSpacerItem(25, 25, QSizePolicy.Minimum, QSizePolicy.Minimum))
        v_lay_sup_dx.addWidget(self.get_label_info("Stato", self.controller.get_stato_cliente()))
        v_lay_sup_dx.addStretch()
        h_lay_sup.addLayout(v_lay_sup_sx)
        h_lay_sup.addLayout(v_lay_sup_dx)
        # layout centrale
        h_lay_cent = QHBoxLayout()
        v_lay_cent_sx = QVBoxLayout()
        v_lay_cent_dx = QVBoxLayout()
        v_lay_cent_sx.addWidget(self.get_label_info("Codice Fiscale", self.controller.get_cf_cliente()))
        v_lay_cent_dx.addWidget(QLabel(""))
        v_lay_cent_sx.addWidget(self.get_label_info("Nato a ", self.controller.get_luogo_nascita_cliente()))
        v_lay_cent_dx.addWidget(self.get_label_info("il ", self.controller.get_data_nascita_cliente()))
        v_lay_cent_sx.addWidget(self.get_label_info("Residente a ", self.controller.get_residenza_cliente()))
        v_lay_cent_dx.addWidget(self.get_label_info("In via ", self.controller.get_indirizzo_cliente()))
        v_lay_cent_sx.addWidget(self.get_label_info("Telefono", self.controller.get_telefono_cliente()))
        v_lay_cent_dx.addWidget(self.get_label_info("Email", self.controller.get_email_cliente()))
        h_lay_cent.addLayout(v_lay_cent_sx)
        h_lay_cent.addLayout(v_lay_cent_dx)
        # layout inferiore
        v_lay_inf = QVBoxLayout()
        v_lay_inf.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        v_lay_inf.addWidget(VistaAbbonamento(self.controller.get_abbonamento_cliente(), self.controller.aggiungi_abbonamento_cliente))
        v_lay_inf.addItem(QSpacerItem(20, 20, QSizePolicy.Minimum, QSizePolicy.Minimum))
        v_lay_inf.addWidget(VistaCertificato(self.controller.get_certificato_cliente(), self.controller.aggiungi_certificato_cliente))
        # layout pulsanti
        h_lay_btn = QHBoxLayout()
        btn_chiudi = QPushButton("Chiudi")
        btn_chiudi.setStyleSheet("background-color: #b0c4de; font-size: 13px; font-weight: bold;")
        btn_chiudi.clicked.connect(self.funz_chiudi)
        btn_elimina = QPushButton("Elimina")
        btn_elimina.setStyleSheet("background-color: #f08080; font-size: 13px; font-weight: bold;")
        btn_elimina.clicked.connect(self.elimina_cliente_click)
        h_lay_btn.addWidget(btn_chiudi)
        h_lay_btn.addWidget(btn_elimina)

        # aggiunta layout minori a quello generale
        self.v_layout.addLayout(h_lay_sup)
        self.v_layout.addLayout(h_lay_cent)
        self.v_layout.addLayout(v_lay_inf)
        self.v_layout.addLayout(h_lay_btn)

        self.setLayout(self.v_layout)

    def get_label_info(self, testo, valore):
        current_label = QLabel("{}: {}".format('<b>{}</b>'.format(testo), valore))
        font_nome = current_label.font()
        current_label.setFont(font_nome)
        current_font = current_label.font()
        current_font.setPointSize(18)
        current_label.setFont(current_font)
        return current_label
    # funzione pulsante elimina
    def elimina_cliente_click(self):
        reply = QMessageBox.question(self, "Messaggio",
                                     "Sicuro di voler eliminare il cliente? OPERAZIONE IRREVERSIBILE", QMessageBox.Yes |
                                     QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.elimina_cliente(self.controller.get_id_cliente())
            self.elimina_callback()
            from listaclienti.views.VistaListaClienti import VistaListaClienti
            VistaListaClienti.profilo_cliente = False
            self.close()
        else:
            pass

    def funz_chiudi(self):
        self.close()
        from listaclienti.views.VistaListaClienti import VistaListaClienti
        VistaListaClienti.profilo_cliente = False
        ControlloreListaClienti().save_data()
