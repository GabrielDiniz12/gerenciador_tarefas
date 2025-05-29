import json
from package.models import Tarefa
from datetime import date, datetime

class RepositorioTarefas:

    @staticmethod
    def tarefa_para_dict(tarefa: Tarefa):
        return {
            "id": tarefa.get_id(),
            "titulo": tarefa.get_titulo(),
            "descricao": tarefa.get_descricao(),
            "data_limite": tarefa.get_data_limite().strftime("%d-%m-%Y"),
            "concluida": tarefa.esta_concluida()
        }

    @staticmethod
    def dict_para_tarefa(dados: dict):
        t = Tarefa(
            id=dados["id"],
            titulo=dados["titulo"],
            descricao=dados["descricao"],
            data_limite=datetime.strptime(dados["data_limite"], "%d-%m-%Y").date(),
        )
        if dados["concluida"]:
            t.concluir()
        return t

    @staticmethod
    def salvar_em_arquivo(lista_tarefas, caminho_arquivo: str):
        lista_dicts = [RepositorioTarefas.tarefa_para_dict(t) for t in lista_tarefas]
        with open(caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(lista_dicts, f, indent=4, ensure_ascii=False)

    @staticmethod
    def carregar_do_arquivo(caminho_arquivo: str):
        try:
            with open(caminho_arquivo, "r", encoding="utf-8") as f:
                lista_dicts = json.load(f)
                return [RepositorioTarefas.dict_para_tarefa(d) for d in lista_dicts]
        except FileNotFoundError:
            return []
