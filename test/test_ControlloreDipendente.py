from unittest import TestCase

from dipendente.model.Dipendente import Dipendente
from listadipendenti.controller.ControlloreListaDipendenti import ControlloreListaDipendenti
from listadipendenti.model.ListaDipendenti import ListaDipendenti


class TestControlloreDipendente(TestCase):

    def setUp(self):
        self.lista = ListaDipendenti()

    # test se il dipendente è aggiunto correttamente
    def test_aggiungi_dip(self):
        self.dip = Dipendente("Rob", "must", "20-05-2000", "tm", "tm", "tm", "mstrrt00e20l113w", "1234567890", "Rob",
                              "collaboratore", "r")
        self.lista.aggiungi_dipendente(self.dip)
        self.assertIsNotNone(self.dip, "non esiste")

    # test di uguaglianza tra due nuovi dipendenti
    def test_confronta_dip(self):
        self.nuovo_dip = Dipendente("Rob", "must", "20-05-2000", "tm", "tm", "tm", "mstrrt00e20l113w", "1234567890",
                                    "Rob", "collaboratore", "r")
        self.nuovo_dip1 = Dipendente("fra", "must", "20-05-2000", "tm", "tm", "tm", "mstrrt00e20l113w", "1234567890",
                                     "Rob", "collaboratore", "r")
        self.assertNotEqual(self.nuovo_dip, self.nuovo_dip1, "dipendente già esistente")

    # test that the list is not null
    def test_list_null(self):
        self.nuovo_dip2 = Dipendente("fra", "must", "20-05-2000", "tm", "tm", "tm", "mstrrt00e20l113w", "1234567890",
                                     "Rob", "collaboratore", "r")
        self.lista.aggiungi_dipendente(self.nuovo_dip2)
        self.assertNotEmpty(self.lista)

    def test_elimina_dipendente(self):
        self.controller = ControlloreListaDipendenti()
        self.dip = Dipendente("rob","must","20-05-2000","tm","tm","tm","mstrrt00e20l113w","1234567890","Rob","collaboratore","r")
        self.controller.aggiungi_dipendente(self.dip)
        self.controller.rimuovi_dalla_lista(self.dip)
        self.assertEmpty(self.controller.get_lista_dipendenti())

    def assertEmpty(self, obj):
        self.assertFalse(obj)

    def assertNotEmpty(self, obj):
       self.assertTrue(obj)