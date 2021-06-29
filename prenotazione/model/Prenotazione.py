from listaprenotazioni.controller.ControlloreListaPrenotazioni import ControlloreListaPrenotazioni


class Prenotazione():
    def __init__(self, nome, cognome, documento, campo, data, ora_inizio):
        self.controllore = ControlloreListaPrenotazioni()
        self.index = self.get_ultimo_id()
        self.index +=1
        self.id = self.index
        self.nome = nome
        self.cognome = cognome
        self.documento = documento
        self.campo = campo
        self.data = data
        self.ora_inizio = ora_inizio
        self.ora_fine = self.calcola_ora_fine()

    def get_ultimo_id(self):
        if not self.controllore.get_lista_prenotazioni():
            return 0
        else:
            indice = len(self.controllore.get_lista_prenotazioni())-1
            prenotazione = self.controllore.get_prenotazione_by_index(indice)
            id = prenotazione.id
            return id

    def calcola_ora_fine(self):
        appoggio = self.ora_inizio.split(":")
        ora = int(appoggio[0])
        minuto = int(appoggio[1])
        minuti = minuto + 30
        if minuti == 60:
            minuti = "00"
            ora = ora + 2
            self.ora_fine = "{}:{}".format(ora, minuti)
            return self.ora_fine
        else:
            ora = ora + 1
            self.ora_fine = "{}:{}".format(ora, minuti)
            return self.ora_fine

    def prezzi_campi(self):
        if self.campo.tipo == "Calcio":
            prezzo = 80
            return prezzo
        elif self.campo.tipo == "Calcetto":
            prezzo = 50
            return prezzo
        else:
            prezzo = 40
            return prezzo