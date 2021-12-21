from unittest import TestCase

from abbonamento.model.Abbonamento import Abbonamento
from certificato.model.Certificato import Certificato
from cliente.model.Cliente import Cliente


class TestControlloreCliente(TestCase):
    #L'abbonamento viene aggiunto correttamente
    def test_aggiungi_abbonamento_cliente(self):
        self.cliente=Cliente("carlogissi", "carlo", "gissi", "cccccccccccccccc", "17-10-2000", "Termoli", "Montecilfone", "bb", "avava", "0000000000")
        self.assertIsNone(self.cliente.abbonamento)
        self.cliente.aggiungi_abbonamento(Abbonamento("21/12/2021", "mensile", 30))
        self.assertIsNotNone(self.cliente.abbonamento)

    # Il certificato viene aggiunto correttamente
    def test_aggiungi_certifiato_cliente(self):
        self.cliente = Cliente("carlogissi", "carlo", "gissi", "cccccccccccccccc", "17-10-2000", "Termoli", "Montecilfone", "bb", "avava", "0000000000")
        self.assertIsNone(self.cliente.certificato)
        self.cliente.aggiungi_certificato(Certificato("21/12/2021"))
        self.assertIsNotNone(self.cliente.certificato)

