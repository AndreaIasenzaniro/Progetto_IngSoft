import json


class Amministratore():
    def __init__(self):

        with open('amministratore/data/login_amministratore.json') as f:
            ammin = json.load(f)
        for campo in ammin:
            self.username = campo["username"]
            self.password = campo["password"]

    def get_username(self):
        return self.username

    def get_password(self):
        return self.password
