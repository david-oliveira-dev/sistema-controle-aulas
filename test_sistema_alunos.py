"""Testes automatizados do Sistema de Controle de Aulas.

Usa apenas a biblioteca padrão (módulo unittest), então roda em qualquer
máquina com Python, sem instalar nada.

Como rodar (dentro da pasta notebooks):

    python3 -m unittest -v

Ou rodando este arquivo direto:

    python3 test_sistema_alunos.py
"""

import os
import tempfile
import unittest

from sistema_alunos import SEMANAS_NO_MES, Aluno, SistemaAlunos


class TestAluno(unittest.TestCase):
    """Testa a classe Aluno: criação, validação e cálculo."""

    def test_cria_aluno_valido(self):
        aluno = Aluno("Ana", "9º ano", "Matemática", 130.0, 2)
        self.assertEqual(aluno.nome, "Ana")
        self.assertEqual(aluno.valor_aula, 130.0)
        self.assertEqual(aluno.aulas_por_semana, 2)

    def test_valor_mensal(self):
        aluno = Aluno("Ana", "9º ano", "Matemática", 130.0, 2)
        esperado = 130.0 * 2 * SEMANAS_NO_MES  # 1040.0
        self.assertEqual(aluno.valor_mensal(), esperado)

    def test_nome_vazio_gera_erro(self):
        with self.assertRaises(ValueError):
            Aluno("   ", "9º ano", "Matemática", 130.0, 2)

    def test_valor_aula_negativo_gera_erro(self):
        with self.assertRaises(ValueError):
            Aluno("Ana", "9º ano", "Matemática", -10, 2)

    def test_aulas_zero_gera_erro(self):
        with self.assertRaises(ValueError):
            Aluno("Ana", "9º ano", "Matemática", 130.0, 0)

    def test_valor_aula_nao_numerico_gera_erro(self):
        with self.assertRaises(ValueError):
            Aluno("Ana", "9º ano", "Matemática", "abc", 2)

    def test_to_dict_e_from_dict(self):
        aluno = Aluno("Ana", "9º ano", "Matemática", 130.0, 2)
        copia = Aluno.from_dict(aluno.to_dict())
        self.assertEqual(copia.to_dict(), aluno.to_dict())


class TestSistemaAlunos(unittest.TestCase):
    """Testa o CRUD e os relatórios do SistemaAlunos."""

    def setUp(self):
        # Cada teste começa com um sistema limpo e dois alunos.
        self.sistema = SistemaAlunos()
        self.sistema.cadastrar("Ana", "9º ano", "Matemática", 130.0, 2)
        self.sistema.cadastrar("João", "8º ano", "Ciências", 120.0, 1)

    def test_cadastrar_aumenta_lista(self):
        self.assertEqual(len(self.sistema.alunos), 2)

    def test_buscar_ignora_maiusculas(self):
        self.assertIsNotNone(self.sistema.buscar("ana"))
        self.assertIsNotNone(self.sistema.buscar("ANA"))
        self.assertIsNone(self.sistema.buscar("Carlos"))

    def test_remover_existente(self):
        self.assertTrue(self.sistema.remover("Ana"))
        self.assertEqual(len(self.sistema.alunos), 1)

    def test_remover_inexistente(self):
        self.assertFalse(self.sistema.remover("Carlos"))
        self.assertEqual(len(self.sistema.alunos), 2)

    def test_editar_aluno(self):
        self.assertTrue(self.sistema.editar("Ana", valor_aula=140.0, aulas_por_semana=3))
        aluno = self.sistema.buscar("Ana")
        self.assertEqual(aluno.valor_aula, 140.0)
        self.assertEqual(aluno.aulas_por_semana, 3)

    def test_editar_com_dado_invalido_gera_erro(self):
        with self.assertRaises(ValueError):
            self.sistema.editar("Ana", valor_aula=-5)

    def test_total_mensal(self):
        # Ana: 130*2*4 = 1040 | João: 120*1*4 = 480 | total = 1520
        self.assertEqual(self.sistema.total_mensal(), 1520.0)

    def test_relatorio_contem_nomes(self):
        texto = self.sistema.relatorio()
        self.assertIn("Ana", texto)
        self.assertIn("João", texto)
        self.assertIn("Total mensal", texto)


class TestPersistencia(unittest.TestCase):
    """Testa salvar e carregar em um arquivo temporário (não mexe no real)."""

    def setUp(self):
        # Cria um arquivo temporário só para o teste.
        fd, self.caminho = tempfile.mkstemp(suffix=".json")
        os.close(fd)

    def tearDown(self):
        if os.path.exists(self.caminho):
            os.remove(self.caminho)

    def test_salvar_e_carregar(self):
        sistema = SistemaAlunos(arquivo=self.caminho)
        sistema.cadastrar("Ana", "9º ano", "Matemática", 130.0, 2)
        sistema.cadastrar("Maria", "1ª série EM", "Física", 150.0, 1)
        sistema.salvar()

        # Um novo sistema deve recuperar exatamente os mesmos dados.
        outro = SistemaAlunos(arquivo=self.caminho)
        outro.carregar()
        self.assertEqual(len(outro.alunos), 2)
        self.assertEqual(outro.buscar("Ana").valor_aula, 130.0)
        self.assertEqual(outro.total_mensal(), sistema.total_mensal())

    def test_carregar_arquivo_inexistente_comeca_vazio(self):
        sistema = SistemaAlunos(arquivo="arquivo_que_nao_existe_123.json")
        sistema.carregar()
        self.assertEqual(sistema.alunos, [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
