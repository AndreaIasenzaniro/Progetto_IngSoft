from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QSpacerItem, QSizePolicy, QPushButton

from dipendente.controller.ControlloreDipendente import ControlloreDipendente


class VistaDipendente(QWidget):
    def __init__(self, dipendente, elimina_dipendente, elimina_callback, parent=None):
        super(VistaDipendente, self).__init__(parent)

        self.controller = ControlloreDipendente(dipendente)
        self.elimina_dipendente = elimina_dipendente
        self.elimina_callback = elimina_callback

        v_layout = QVBoxLayout()

        label_name = QLabel(self.controller.get_nome_dipendente() +" "+ self.controller.get_cognome_dipendente())

        # inserimento sfondo
        image = QLabel(self)
        image.setGeometry(0, 0, 500, 600)
        pixmap = QPixmap("dipendente/views/dip.jpg")
        image.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        image.show()
        # fisso la finestra alle dimensioni della foto
        self.setFixedSize(500, 600)
        # self.showMaximized()

        # creazione pulsante di elimina del cliente
        btn_elimina = QPushButton("Elimina")
        btn_elimina.setStyleSheet("background-color: #f08080; font-size: 15px; font-weight: bold;")
        btn_elimina.clicked.connect(self.elimina_dipendente_click)


        # aggiunta oggetti al layout
        v_layout.addWidget(label_name)
        v_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        v_layout.addWidget(self.get_label_info("ID", self.controller.get_id_dipendente()))
        v_layout.addWidget(self.get_label_info("Codice Fiscale", self.controller.get_cf_dipendente()))
        v_layout.addWidget(self.get_label_info("Data di nascita", self.controller.get_data_dipendente()))
        v_layout.addWidget(self.get_label_info("Luogo di nascita", self.controller.get_luogo_dipendente()))
        v_layout.addWidget(self.get_label_info("Email", self.controller.get_email_dipendente()))
        v_layout.addWidget(self.get_label_info("Telefono", self.controller.get_telefono_dipendente()))
        v_layout.addWidget(self.get_label_info("Abilitazione", self.controller.get_abilitazione_dipendente()))
        #password del dipendente non visibile!!
        v_layout.addItem(QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding))
        v_layout.addWidget(btn_elimina)

        self.setLayout(v_layout)
        self.setWindowTitle("Scheda: " + self.controller.get_nome_dipendente() + " " + self.controller.get_cognome_dipendente())

    def get_label_info(self, testo, valore):
        current_label = QLabel("{}: {}".format(testo, valore))
        current_font = current_label.font()
        current_font.setPointSize(17)
        current_label.setFont(current_font)
        return current_label

    def elimina_dipendente_click(self):
        self.elimina_dipendente(self.controller.get_id_dipendente())
        self.elimina_callback()
        self.close()