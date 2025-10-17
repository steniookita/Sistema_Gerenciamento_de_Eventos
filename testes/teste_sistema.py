import unittest
from datetime import datetime, timedelta
from Sistema_Gerenciamento_de_Eventos import Evento, Workshop, Palestra, Participante  

class TestEvento(unittest.TestCase):

    def setUp(self):
        self.evento = Evento(
            nome="TechConf",
            data=(datetime.now() + timedelta(days=5)).strftime('%Y-%m-%d %H:%M:%S'),
            local="Recife",
            categoria="Tecnologia",
            capacidade_max=3,
            preco=100.0
        )
        
        self.evento._Evento__participantes = []

    def test_criacao_evento_valido(self):
        self.assertEqual(self.evento.get_nome(), "TechConf")
        self.assertEqual(self.evento.get_local(), "Recife")
        self.assertEqual(self.evento.get_preco(), 100.0)

    def test_capacidade_invalida(self):
        with self.assertRaises(ValueError):
            Evento("Show", "2025-12-12 19:00:00", "Arena", "Música", 0, 150)

    def test_preco_negativo(self):
        with self.assertRaises(ValueError):
            Evento("Feira", "2025-12-12 19:00:00", "Centro", "Cultura", 100, -10)

    def test_get_data_formatada(self):
        data_formatada = self.evento.get_data_formatada()
        self.assertRegex(data_formatada, r'\d{2}/\d{2}/\d{4}')

    def test_inscricao_participante(self):
        p1 = Participante("Ana", "ana@email.com")
        self.evento.inscrever_participante(p1)
        self.assertEqual(self.evento.total_inscritos(), 1)

    def test_inscricao_participante_duplicado(self):
        p1 = Participante("Ana", "ana@email.com")
        self.evento.inscrever_participante(p1)
        with self.assertRaises(Exception):
            self.evento.inscrever_participante(p1)

    def test_evento_lotado(self):
        p1 = Participante("A", "a@email.com")
        p2 = Participante("B", "b@email.com")
        p3 = Participante("C", "c@email.com")
        p4 = Participante("D", "d@email.com")

        self.evento.inscrever_participante(p1)
        self.evento.inscrever_participante(p2)
        self.evento.inscrever_participante(p3)
        with self.assertRaises(Exception):
            self.evento.inscrever_participante(p4)

    def test_cancelar_inscricao(self):
        p1 = Participante("Ana", "ana@email.com")
        self.evento.inscrever_participante(p1)
        self.evento.cancelar_inscricao("ana@email.com")
        self.assertEqual(self.evento.total_inscritos(), 0)

    def test_cancelar_participante_inexistente(self):
        with self.assertRaises(Exception):
            self.evento.cancelar_inscricao("naoexiste@email.com")

    def test_receita_total(self):
        p1 = Participante("A", "a@email.com")
        p2 = Participante("B", "b@email.com")
        self.evento.inscrever_participante(p1)
        self.evento.inscrever_participante(p2)
        self.assertEqual(self.evento.receita_total(), 200.0)


class TestSubclasses(unittest.TestCase):

    def test_workshop_detalhes(self):
        w = Workshop("Oficina Python", "2025-12-12 10:00:00", "Recife", 20, "Educação", 0, "Notebook")
        self.assertIn("Material necessário", w.detalhes())

    def test_palestra_detalhes(self):
        p = Palestra("Inteligência Artificial", "2025-12-12 10:00:00", "Recife", 100, "Tecnologia", 0, "Dra. Souza")
        self.assertIn("Palestrante", p.detalhes())


class TestParticipante(unittest.TestCase):

    def test_check_in(self):
        p = Participante("Carlos", "carlos@email.com")
        self.assertFalse(p.check_in_realizado())
        p.realizar_check_in()
        self.assertTrue(p.check_in_realizado())


if __name__ == '__main__':
    unittest.main()
