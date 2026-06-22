# Sistema de Controle de Aulas

[![CI](https://github.com/david-oliveira-dev/sistema-controle-aulas/actions/workflows/ci.yml/badge.svg)](https://github.com/david-oliveira-dev/sistema-controle-aulas/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.11%20%7C%203.12-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Projeto de estudos em **Engenharia de Software**, construído de forma progressiva
em Python. A ideia é simular um sistema real de controle de alunos particulares:
cadastrar alunos, calcular o valor mensal de cada um, gerar relatórios e salvar
os dados em arquivo.

O projeto evolui passo a passo, do básico (variáveis e listas) até um sistema
organizado com **orientação a objetos**, **validação**, **tratamento de erros** e
**testes automatizados**.

## Trilha de notebooks

| Notebook | Tema | O que foi aprendido |
|----------|------|---------------------|
| `01_primeiros_estudos_python.ipynb` | Fundamentos | variáveis, listas, dicionários, `for`, funções, primeiro relatório |
| `02_funcoes_e_arquivos.ipynb` | Funções e arquivos | cadastro com funções, salvar/carregar JSON, formatação de valores |
| `03_sistema_com_menu.ipynb` | Sistema interativo | menu com `while`, `input()`, CRUD completo (cadastrar, listar, editar, remover) |
| `04_validacao_e_tratamento_de_erros.ipynb` | Robustez | `try`/`except`, validação de dados, `raise`, entrada segura |
| `05_orientacao_a_objetos.ipynb` | POO | classes `Aluno` e `SistemaAlunos`, métodos, `__str__`, `to_dict`/`from_dict` |

## Sistema final (código de produção)

- **`sistema_alunos.py`** — versão final do sistema, organizada em classes, com
  validação, persistência em JSON e menu interativo.
- **`test_sistema_alunos.py`** — testes automatizados (17 testes) usando `unittest`.
- **`alunos.json`** — base de dados de exemplo.

### Como executar o sistema

Dentro desta pasta (`notebooks/`):

```bash
python3 sistema_alunos.py
```

Abre o menu interativo no terminal.

### Como rodar os testes

```bash
python3 -m unittest -v
```

Todos os testes usam apenas a biblioteca padrão do Python — não é preciso instalar
nada.

### Como usar como módulo (em um notebook ou script)

```python
from sistema_alunos import Aluno, SistemaAlunos

sistema = SistemaAlunos()          # usa "alunos.json" por padrão
sistema.carregar()                 # lê os alunos salvos
sistema.cadastrar("Ana", "9º ano", "Matemática", 130.0, 2)
print(sistema.relatorio())
sistema.salvar()
```

## Regra de cálculo

```
valor mensal = valor da aula × aulas por semana × 4 (semanas no mês)
```

## Próximos passos

- substituir o JSON por banco de dados **SQLite**;
- transformar o sistema em uma **API** (FastAPI / Flask);
- adicionar interface gráfica ou web;
- versionar o projeto com **Git/GitHub**.

## 📫 Contato

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0A66C2?style=flat&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/david-oliveira-9970a42a5)
[![GitHub](https://img.shields.io/badge/GitHub-181717?style=flat&logo=github&logoColor=white)](https://github.com/david-oliveira-dev)
