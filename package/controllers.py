from package.models import Tarefa
from datetime import date
import json

class GerenciadorTarefas: # Responsável por gerenciar várias tarefas
    def __init__(self):
        self._tarefas = [] # Composição forte: as tarefas existem dentro do gerenciador

    def add_tarefa(self, tarefa: Tarefa):
        self._tarefas.append(tarefa) # Adiciona uma nova tarefa

    def remover_tarefa(self, id_tarefa: int):
        self._tarefas = [t for t in self._tarefas if t.get_id() != id_tarefa] # Remove a tarefa com o id específicado, caso exista

    def buscar_por_id(self, id_tarefa: int):
        for tarefa in self._tarefas: #Associação fraca
            if tarefa.get_id() == id_tarefa:
                return tarefa
        return None
    
    def listar_tarefas(self):
        return self._tarefas
    
    def substituir_tarefas(self, nova_lista):
        self._tarefas = nova_lista

    def editar_tarefa(self, id_tarefa: int, titulo: str, descricao: str, data_limite: date) -> bool: # Busca a tarefa por ID e atualiza seus campos.Retorna True se encontrou e editou, False caso contrário.
        tarefa = self.buscar_por_id(id_tarefa)
        if not tarefa:
            return False
        tarefa.set_titulo(titulo)
        tarefa.set_descricao(descricao)
        tarefa.set_data_limite(data_limite)
        return True
    
    def tarefas_atrasadas(self):
        return [t for t in self._tarefas if not t.esta_concluida() and date.today() > t.get_data_limite_obj()]