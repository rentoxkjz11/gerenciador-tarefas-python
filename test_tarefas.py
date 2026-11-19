"""Testes automáticos do gerenciador de tarefas.

Como executar:
    python -m unittest -v
"""

import tempfile
import unittest
from pathlib import Path

from tarefas import GerenciadorTarefas


class TestGerenciadorTarefas(unittest.TestCase):
    def setUp(self):
        # Cada teste usa um arquivo temporário, sem mexer no seu tarefas.json real.
        self.pasta = tempfile.TemporaryDirectory()
        self.arquivo = Path(self.pasta.name) / "tarefas.json"
        self.g = GerenciadorTarefas(self.arquivo)

    def tearDown(self):
        self.pasta.cleanup()

    def test_adicionar_tarefa(self):
        tarefa = self.g.adicionar("Estudar Python", "alta")
        self.assertEqual(tarefa.id, 1)
        self.assertEqual(tarefa.prioridade, "alta")
        self.assertFalse(tarefa.concluida)
        self.assertEqual(len(self.g.listar()), 1)

    def test_titulo_vazio_gera_erro(self):
        with self.assertRaises(ValueError):
            self.g.adicionar("   ")

    def test_prioridade_invalida_gera_erro(self):
        with self.assertRaises(ValueError):
            self.g.adicionar("Teste", "urgentissima")

    def test_ids_sequenciais(self):
        a = self.g.adicionar("A")
        b = self.g.adicionar("B")
        self.assertEqual((a.id, b.id), (1, 2))

    def test_concluir_tarefa(self):
        tarefa = self.g.adicionar("Fazer exercícios")
        self.g.concluir(tarefa.id)
        self.assertTrue(self.g.listar()[0].concluida)
        self.assertEqual(self.g.listar(somente_pendentes=True), [])

    def test_remover_tarefa(self):
        tarefa = self.g.adicionar("Apagar depois")
        self.g.remover(tarefa.id)
        self.assertEqual(self.g.listar(), [])

    def test_id_inexistente_gera_erro(self):
        with self.assertRaises(ValueError):
            self.g.concluir(99)
        with self.assertRaises(ValueError):
            self.g.remover(99)

    def test_dados_persistem_no_arquivo(self):
        self.g.adicionar("Salvar no arquivo", "baixa")
        outro = GerenciadorTarefas(self.arquivo)  # lê o mesmo arquivo
        self.assertEqual(len(outro.listar()), 1)
        self.assertEqual(outro.listar()[0].titulo, "Salvar no arquivo")

    def test_arquivo_corrompido_nao_quebra_o_programa(self):
        self.arquivo.write_text("isto não é json", encoding="utf-8")
        g = GerenciadorTarefas(self.arquivo)
        self.assertEqual(g.listar(), [])


if __name__ == "__main__":
    unittest.main()
