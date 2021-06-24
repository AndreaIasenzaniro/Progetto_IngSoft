from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, QSpacerItem, QSizePolicy

from abbonamento.views.VistaAbbonamento import VistaAbbonamento
from certificato.views.VistaCertificato import VistaCertificato
from cliente.controller.ControlloreCliente import ControlloreCliente


class VistaCliente(QWidget):
    def __init__(self, cliente, elimina_cliente, elimina_callback, parent=None):
        super(VistaCliente, self).__init__(parent)

        #self.setFixedSize(750, 580)

        self.controller = ControlloreCliente(cliente)
        self.elimina_cliente = elimina_cliente
        self.elimina_callback = elimina_callback
        # layout verticale principale
        self.v_layout = QVBoxLayout()
        # immagine profilo cliente
        self.label_img = QLabel()
        self.label_img.setPixmap(QPixmap('listaclienti/data/utente.png'))
        # titolo scheda profilo cliente
        self.setWindowTitle("Scheda cliente: " + self.controller.get_nome_cliente() + " " + self.controller.get_cognome_cliente())

        # nome cliente visualizzato in grande
        label_nome = QLabel(self.controller.get_nome_cliente() + " " + self.controller.get_cognome_cliente())
        font_nome = label_nome.font()
        font_nome.setPointSize(20)
        label_nome.setFont(font_nome)

        # layout di visualizzazione superiore
        h_lay_sup = QHBoxLayout()
        v_lay_sup_sx = QVBoxLayout()
        v_lay_sup_dx = QVBoxLayout()
        v_lay_sup_sx.addWidget(self.label_img)
        v_lay_sup_dx.addItem(QSpacerItem(65, 65, QSizePolicy.Minimum, QSizePolicy.Minimum))
        v_lay_sup_dx.addWidget(label_nome)
        v_lay_sup_dx.addItem(QSpacerItem(25, 25, QSizePolicy.Minimum, QSizePolicy.Minimum))
        v_lay_sup_dx.addWidget(self.get_label_info("Stato", self.controller.get_stato_cliente()))
        v_lay_sup_dx.addStretch()
        h_lay_sup.addLayout(v_lay_sup_sx)
        h_lay_sup.addLayout(v_lay_sup_dx)

        # layout di visualizzazione centrale
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

        # layout di visualizzazione inferiore
        v_lay_inf = QVBoxLayout()
        v_lay_inf.addItem(QSpacerItem(15, 15, QSizePolicy.Minimum, QSizePolicy.Minimum))
        #v_lay_inf.addWidget(QLabel("<b>ABBONAMENTO - INGRESSO</b>"))
        v_lay_inf.addWidget(VistaAbbonamento(self.controller.get_abbonamento_cliente(), self.controller.aggiungi_abbonamento_cliente))
        v_lay_inf.addItem(QSpacerItem(15, 15, QSizePolicy.Minimum, QSizePolicy.Minimum))
        #v_lay_inf.addWidget(QLabel("<b>CERTIFICATO MEDICO</b>"))
        v_lay_inf.addWidget(VistaCertificato(self.controller.get_certificato_cliente(),self.controller.aggiungi_certificato_cliente))

        # layout di visualizzazione per pulsanti
        h_lay_btn = QHBoxLayout()
        btn_chiudi = QPushButton("Chiudi")
        btn_chiudi.clicked.connect(self.close)
        btn_elimina = QPushButton("Elimina")
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
        current_font.setPointSize(15)
        current_label.setFont(current_font)
        return current_label

    '''def check_abbonamento(self):
        self.vista_abbonamento = VistaAbbonamento(self.controller.get_abbonamento_cliente(), self.controller.aggiungi_abbonamento_cliente)
        self.vista_abbonamento.show()
        self.vista_abbonamento.setWindowTitle("Abbonamento: " + self.controller.get_nome_cliente() + " " + self.controller.get_cognome_cliente())
        #self.update()

    def check_certificato(self):
        self.vista_certificato = VistaCertificato(self.controller.get_certificato_cliente(), self.controller.aggiungi_certificato_cliente)
        self.vista_certificato.show()
        self.vista_certificato.setWindowTitle("Certificato: " + self.controller.get_nome_cliente() + " " + self.controller.get_cognome_cliente())'''

    def elimina_cliente_click(self):
        self.elimina_cliente(self.controller.get_id_cliente())
        self.elimina_callback()
        self.close()
