import sys
from PyQt5.QtWidgets import QApplication
from home.login.Login import Login
stylesheet = """
    VistaHome {
        background-image: url("home/views/Logo_Università_Politecnica_delle_Marche.png"); 
    }
"""

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)

    login = Login()
    #la prima volta mostriamo a prescindere il form del login
    #da qui in poi ogni volta che la password sarà errata mostreremo nuovamente il form del login altrimenti mostriamo la nuova pagina
    login.show()
    #if login.check_password() == True:
    #login.close()
    #vistaHome = VistaHome()
    #vistaHome.setStyleSheet(stylesheet)
    #vistaHome.show()
    sys.exit(app.exec())
