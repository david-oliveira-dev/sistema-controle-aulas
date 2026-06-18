"""Sistema de Controle de Aulas — versão final (orientada a objetos).

Este módulo é a evolução do projeto desenvolvido nos notebooks 01 a 05.
Aqui o código de controle de alunos foi reorganizado em classes, com
validação de dados, tratamento de erros e persistência em arquivo JSON.

Pode ser usado de duas formas:

1. Importando as classes em um notebook ou em outro script:

       from sistema_alunos import Aluno, SistemaAlunos

2. Executando direto no terminal (abre o menu interativo):

       python3 sistema_alunos.py
"""

import json

# Constantes do sistema (evita "números mágicos" espalhados pelo código).
SEMANAS_NO_MES = 4
ARQUIVO_PADRAO = "alunos.json"


class Aluno:
    """Representa um aluno particular e seus dados de cobrança."""

    def __init__(self, nome, serie, disciplina, valor_aula, aulas_por_semana):
        # A validação acontece aqui: não é possível criar um Aluno inválido.
        self.nome = self._validar_texto(nome, "nome")
        self.serie = self._validar_texto(serie, "série")
        self.disciplina = self._validar_texto(disciplina, "disciplina")
        self.valor_aula = self._validar_valor_aula(valor_aula)
        self.aulas_por_semana = self._validar_aulas(aulas_por_semana)

    # ------------------------------------------------------------------
    # Validações (métodos "privados", por convenção começam com _)
    # ------------------------------------------------------------------
    @staticmethod
    def _validar_texto(valor, campo):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"O campo '{campo}' não pode ficar vazio.")
        return valor.strip()

    @staticmethod
    def _validar_valor_aula(valor):
        try:
            valor = float(valor)
        except (TypeError, ValueError):
            raise ValueError("O valor da aula precisa ser um número.") from None
        if valor <= 0:
            raise ValueError("O valor da aula precisa ser maior que zero.")
        return valor

    @staticmethod
    def _validar_aulas(valor):
        try:
            valor = int(valor)
        except (TypeError, ValueError):
            raise ValueError("As aulas por semana precisam ser um número inteiro.") from None
        if valor <= 0:
            raise ValueError("As aulas por semana precisam ser maior que zero.")
        return valor

    # ------------------------------------------------------------------
    # Comportamento
    # ------------------------------------------------------------------
    def valor_mensal(self):
        """Valor estimado por mês (considera SEMANAS_NO_MES semanas)."""
        return self.valor_aula * self.aulas_por_semana * SEMANAS_NO_MES

    def to_dict(self):
        """Converte o aluno em dicionário (para salvar em JSON)."""
        return {
            "nome": self.nome,
            "serie": self.serie,
            "disciplina": self.disciplina,
            "valor_aula": self.valor_aula,
            "aulas_por_semana": self.aulas_por_semana,
        }

    @classmethod
    def from_dict(cls, dados):
        """Cria um Aluno a partir de um dicionário (lido do JSON)."""
        return cls(
            nome=dados["nome"],
            serie=dados["serie"],
            disciplina=dados["disciplina"],
            valor_aula=dados["valor_aula"],
            aulas_por_semana=dados["aulas_por_semana"],
        )

    def __str__(self):
        return (
            f"{self.nome} — {self.serie} | {self.disciplina} | "
            f"R$ {self.valor_aula:.2f}/aula | {self.aulas_por_semana}x/semana | "
            f"mensal: R$ {self.valor_mensal():.2f}"
        )


class SistemaAlunos:
    """Gerencia a coleção de alunos: cadastrar, listar, editar, remover."""

    def __init__(self, arquivo=ARQUIVO_PADRAO):
        self.arquivo = arquivo
        self.alunos = []

    # ------------------------------------------------------------------
    # CRUD
    # ------------------------------------------------------------------
    def cadastrar(self, nome, serie, disciplina, valor_aula, aulas_por_semana):
        aluno = Aluno(nome, serie, disciplina, valor_aula, aulas_por_semana)
        self.alunos.append(aluno)
        return aluno

    def buscar(self, nome):
        """Retorna o primeiro aluno com o nome dado (sem diferenciar maiúsculas)."""
        nome = nome.strip().lower()
        for aluno in self.alunos:
            if aluno.nome.lower() == nome:
                return aluno
        return None

    def remover(self, nome):
        aluno = self.buscar(nome)
        if aluno is None:
            return False
        self.alunos.remove(aluno)
        return True

    def editar(self, nome, **novos_dados):
        """Atualiza os campos informados de um aluno já existente.

        Ex.: sistema.editar("Ana", valor_aula=140, aulas_por_semana=3)
        """
        aluno = self.buscar(nome)
        if aluno is None:
            return False
        # Recria o aluno com os dados novos para reaproveitar as validações.
        dados = aluno.to_dict()
        dados.update(novos_dados)
        atualizado = Aluno.from_dict(dados)
        # Substitui no mesmo lugar da lista.
        indice = self.alunos.index(aluno)
        self.alunos[indice] = atualizado
        return True

    # ------------------------------------------------------------------
    # Relatórios
    # ------------------------------------------------------------------
    def total_mensal(self):
        return sum(aluno.valor_mensal() for aluno in self.alunos)

    def relatorio(self):
        """Monta o relatório como texto (string), para imprimir ou testar."""
        linhas = ["", "RELATÓRIO DE ALUNOS", "=" * 40]

        if not self.alunos:
            linhas.append("Nenhum aluno cadastrado.")
            return "\n".join(linhas)

        for aluno in self.alunos:
            linhas.append(f"Nome: {aluno.nome}")
            linhas.append(f"Série: {aluno.serie}")
            linhas.append(f"Disciplina: {aluno.disciplina}")
            linhas.append(f"Valor por aula: R$ {aluno.valor_aula:.2f}")
            linhas.append(f"Aulas por semana: {aluno.aulas_por_semana}")
            linhas.append(f"Valor mensal: R$ {aluno.valor_mensal():.2f}")
            linhas.append("-" * 40)

        linhas.append(f"Total mensal estimado: R$ {self.total_mensal():.2f}")
        return "\n".join(linhas)

    # ------------------------------------------------------------------
    # Persistência (arquivo JSON)
    # ------------------------------------------------------------------
    def salvar(self):
        dados = [aluno.to_dict() for aluno in self.alunos]
        with open(self.arquivo, "w", encoding="utf-8") as arquivo:
            json.dump(dados, arquivo, ensure_ascii=False, indent=4)

    def carregar(self):
        """Carrega os alunos do arquivo. Se não existir, começa vazio."""
        try:
            with open(self.arquivo, encoding="utf-8") as arquivo:
                dados = json.load(arquivo)
        except FileNotFoundError:
            self.alunos = []
            return self.alunos

        self.alunos = [Aluno.from_dict(d) for d in dados]
        return self.alunos


# ----------------------------------------------------------------------
# Funções de entrada com validação (usadas no menu interativo)
# ----------------------------------------------------------------------
def ler_texto(mensagem):
    while True:
        valor = input(mensagem).strip()
        if valor:
            return valor
        print("  -> Esse campo não pode ficar vazio. Tente de novo.")


def ler_float(mensagem):
    while True:
        try:
            valor = float(input(mensagem).replace(",", "."))
        except ValueError:
            print("  -> Digite um número válido (ex.: 130 ou 130.50).")
            continue
        if valor <= 0:
            print("  -> O valor precisa ser maior que zero.")
            continue
        return valor


def ler_int(mensagem):
    while True:
        try:
            valor = int(input(mensagem))
        except ValueError:
            print("  -> Digite um número inteiro (ex.: 2).")
            continue
        if valor <= 0:
            print("  -> O número precisa ser maior que zero.")
            continue
        return valor


# ----------------------------------------------------------------------
# Menu interativo (só roda quando executamos o arquivo diretamente)
# ----------------------------------------------------------------------
def menu():
    sistema = SistemaAlunos()
    sistema.carregar()
    print(f"{len(sistema.alunos)} aluno(s) carregado(s) de '{sistema.arquivo}'.")

    while True:
        print("\nSISTEMA DE CONTROLE DE AULAS")
        print("=" * 40)
        print("1 - Cadastrar aluno")
        print("2 - Listar alunos")
        print("3 - Gerar relatório")
        print("4 - Salvar dados")
        print("5 - Remover aluno")
        print("6 - Editar aluno")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            print("\nCADASTRO DE ALUNO")
            print("=" * 40)
            try:
                sistema.cadastrar(
                    nome=ler_texto("Nome do aluno: "),
                    serie=ler_texto("Série: "),
                    disciplina=ler_texto("Disciplina: "),
                    valor_aula=ler_float("Valor da aula: "),
                    aulas_por_semana=ler_int("Aulas por semana: "),
                )
                print("Aluno cadastrado com sucesso!")
            except ValueError as erro:
                print(f"Erro ao cadastrar: {erro}")

        elif opcao == "2":
            print("\nLISTA DE ALUNOS")
            print("=" * 40)
            if not sistema.alunos:
                print("Nenhum aluno cadastrado.")
            else:
                for aluno in sistema.alunos:
                    print(aluno)

        elif opcao == "3":
            print(sistema.relatorio())

        elif opcao == "4":
            sistema.salvar()
            print(f"Dados salvos em '{sistema.arquivo}'.")

        elif opcao == "5":
            nome = ler_texto("Nome do aluno a remover: ")
            if sistema.remover(nome):
                print("Aluno removido com sucesso!")
            else:
                print("Aluno não encontrado.")

        elif opcao == "6":
            nome = ler_texto("Nome do aluno a editar: ")
            aluno = sistema.buscar(nome)
            if aluno is None:
                print("Aluno não encontrado.")
            else:
                print(f"Editando: {aluno}")
                try:
                    sistema.editar(
                        nome,
                        nome=ler_texto("Novo nome: "),
                        serie=ler_texto("Nova série: "),
                        disciplina=ler_texto("Nova disciplina: "),
                        valor_aula=ler_float("Novo valor da aula: "),
                        aulas_por_semana=ler_int("Novas aulas por semana: "),
                    )
                    print("Aluno atualizado com sucesso!")
                except ValueError as erro:
                    print(f"Erro ao editar: {erro}")

        elif opcao == "0":
            sistema.salvar()
            print("Dados salvos. Encerrando sistema...")
            break

        else:
            print("Opção inválida. Escolha um número do menu.")


if __name__ == "__main__":
    menu()
