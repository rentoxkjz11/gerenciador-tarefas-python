# Gerenciador de Tarefas (Python)

Aplicação de linha de comando para cadastrar, listar, concluir e remover tarefas, com prioridade (baixa, média ou alta). Os dados são salvos em um arquivo JSON, então permanecem depois de fechar o programa.

Projeto de estudo para praticar os fundamentos de Python.

## O que ele faz

- Adiciona tarefas com título e prioridade
- Lista todas as tarefas ou só as pendentes
- Marca tarefas como concluídas
- Remove tarefas
- Salva e carrega as tarefas de um arquivo `tarefas.json`
- Valida entradas (título vazio, prioridade inválida, ID inexistente)

## O que foi praticado

- Funções, classes e `dataclass`
- Leitura e escrita de arquivos JSON
- Tratamento de erros com `try/except` e `ValueError`
- Separação entre regras de negócio (`GerenciadorTarefas`) e interface de terminal
- Testes automáticos com `unittest`

## Tecnologias

Python 3.9 ou superior, usando apenas a biblioteca padrão (`json`, `dataclasses`, `pathlib`, `unittest`). Não precisa instalar nada.

## Como executar

```bash
python tarefas.py
```

No Windows, se `python` não funcionar, tente `py tarefas.py`.

## Como rodar os testes

```bash
python -m unittest -v
```

## Estrutura

```
├── tarefas.py        # programa principal (regras + menu)
├── test_tarefas.py   # testes automáticos
└── README.md
```

## Próximos passos possíveis

- Editar o título de uma tarefa
- Data limite e ordenação por prioridade
- Interface com argumentos de linha de comando (`argparse`)
