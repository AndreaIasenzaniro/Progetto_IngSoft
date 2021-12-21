from unittest import TestCase

from listaprenotazioni.controller.ControlloreListaPrenotazioni import ControlloreListaPrenotazioni
from listaprenotazioni.model.ListaPrenotazioni import ListaPrenotazioni
from prenotazione.model.Prenotazione import Prenotazione


class TestControlloreListaPrenotazioni(TestCase):
    # La prenotazione viene aggiunta correttamente
    def test_aggiungi_prenotazione(self):
        self.lista=ListaPrenotazioni()
        self.prenotazione=Prenotazione("Carlo", "Gissi", "AA", "Calcio", "21-12-2021","10:00")
        self.lista.aggiungi_prenotazione(self.prenotazione)
        self.assertNotEmpty(self.lista)

    # La prenotazione viene eliminata correttamente
    def test_elimina_prenotazione_by_id(self):
        self.controller = ControlloreListaPrenotazioni()
        self.prenotazione = Prenotazione("Carlo", "Gissi", "AA", "Calcio", "21-12-2021", "10:00")
        self.controller.aggiungi_prenotazione(self.prenotazione)
        self.controller.rimuovi_dalla_lista(self.prenotazione)
        self.assertEmpty(self.controller.get_lista_prenotazioni())

    def assertEmpty(self, obj):
        self.assertFalse(obj)

    def assertNotEmpty(self, obj):
        self.assertTrue(obj)

