"""Gerenciador de Tarefas em linha de comando.

Permite cadastrar, listar, concluir e remover tarefas. Os dados ficam
salvos em um arquivo JSON, então continuam existindo depois que o
programa é fechado.

Como executar:
    python tarefas.py
"""

import json
from dataclasses import asdict, dataclass
from pathlib import Path

ARQUIVO_PADRAO = Path("tarefas.json")
PRIORIDADES = ("baixa", "media", "alta")


@dataclass
class Tarefa:
    """Representa uma tarefa da lista."""

    id: int
    titulo: str
    prioridade: str = "media"
    concluida: bool = False


class GerenciadorTarefas:
    """Regras de negócio: não faz print nem input, só manipula tarefas.

    Separar isso da interface (o menu) facilita os testes automáticos.
    """

    def __init__(self, arquivo=ARQUIVO_PADRAO):
        self.arquivo = Path(arquivo)
        self.tarefas = []
        self._carregar()

    # ---------- persistência ----------
    def _carregar(self):
        if not self.arquivo.exists():
            return
        try:
            dados = json.loads(self.arquivo.read_text(encoding="utf-8"))
            self.tarefas = [Tarefa(**item) for item in dados]
        except (json.JSONDecodeError, TypeError, OSError):
            print("Aviso: não foi possível ler o arquivo de tarefas. Começando com a lista vazia.")
            self.tarefas = []

    def _salvar(self):
        dados = [asdict(tarefa) for tarefa in self.tarefas]
        self.arquivo.write_text(
            json.dumps(dados, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    # ---------- operações ----------
    def _buscar(self, id_tarefa):
        for tarefa in self.tarefas:
            if tarefa.id == id_tarefa:
                return tarefa
        raise ValueError(f"Tarefa {id_tarefa} não encontrada.")

    def adicionar(self, titulo, prioridade="media"):
        titulo = titulo.strip()
        if not titulo:
            raise ValueError("O título não pode ficar vazio.")
        if prioridade not in PRIORIDADES:
            raise ValueError(f"Prioridade inválida. Use: {', '.join(PRIORIDADES)}.")

        novo_id = max((t.id for t in self.tarefas), default=0) + 1
        tarefa = Tarefa(id=novo_id, titulo=titulo, prioridade=prioridade)
        self.tarefas.append(tarefa)
        self._salvar()
        return tarefa

    def listar(self, somente_pendentes=False):
        if somente_pendentes:
            return [t for t in self.tarefas if not t.concluida]
        return list(self.tarefas)

    def concluir(self, id_tarefa):
        tarefa = self._buscar(id_tarefa)
        tarefa.concluida = True
        self._salvar()
        return tarefa

    def remover(self, id_tarefa):
        tarefa = self._buscar(id_tarefa)
        self.tarefas.remove(tarefa)
        self._salvar()
        return tarefa


# ---------- interface de terminal ----------
def formatar(tarefa):
    marca = "x" if tarefa.concluida else " "
    return f"[{marca}] #{tarefa.id} {tarefa.titulo} (prioridade: {tarefa.prioridade})"


def ler_inteiro(mensagem):
    """Pede um número ao usuário; devolve None se ele digitar algo inválido."""
    try:
        return int(input(mensagem))
    except ValueError:
        print("Digite um número válido.")
        return None


def mostrar_lista(tarefas):
    if not tarefas:
        print("Nenhuma tarefa por aqui.")
        return
    for tarefa in tarefas:
        print(formatar(tarefa))


def menu():
    print("\n=== Gerenciador de Tarefas ===")
    print("1 - Adicionar tarefa")
    print("2 - Listar todas")
    print("3 - Listar pendentes")
    print("4 - Concluir tarefa")
    print("5 - Remover tarefa")
    print("0 - Sair")
    return input("Escolha uma opção: ").strip()


def main():
    gerenciador = GerenciadorTarefas()

    while True:
        opcao = menu()
        try:
            if opcao == "1":
                titulo = input("Título: ")
                prioridade = input("Prioridade (baixa/media/alta) [media]: ").strip().lower() or "media"
                tarefa = gerenciador.adicionar(titulo, prioridade)
                print(f"Tarefa adicionada: {formatar(tarefa)}")
            elif opcao == "2":
                mostrar_lista(gerenciador.listar())
            elif opcao == "3":
                mostrar_lista(gerenciador.listar(somente_pendentes=True))
            elif opcao == "4":
                id_tarefa = ler_inteiro("ID da tarefa: ")
                if id_tarefa is not None:
                    print(f"Concluída: {formatar(gerenciador.concluir(id_tarefa))}")
            elif opcao == "5":
                id_tarefa = ler_inteiro("ID da tarefa: ")
                if id_tarefa is not None:
                    print(f"Removida: {formatar(gerenciador.remover(id_tarefa))}")
            elif opcao == "0":
                print("Até mais!")
                break
            else:
                print("Opção inválida.")
        except ValueError as erro:
            print(f"Erro: {erro}")


if __name__ == "__main__":
    main()
