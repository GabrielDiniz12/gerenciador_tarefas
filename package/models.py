from datetime import datetime
from datetime import date
class TimestampMixin: # Mixin para registrar timestamps(data/hora)
    def __init__(self):
        self.criado_em = datetime.now() # Armazenando data e hora de criação do objeto
        self.atualizado_em = datetime.now() # Armazenando a data e hora da última modificação

    def touch(self): # Atualizar o 'atualizado_em (última modificação)
        self.atualizado_em = datetime.now()

class Tarefa(TimestampMixin):  # classe principal / herdando TimestampMixin para timestamps
    def __init__(self, id, titulo, descricao, data_limite):
        super().__init__()  # Inicializa o mixin

        # Converte string para date se necessário (espera DD-MM-AAAA)
        if isinstance(data_limite, str):
            data_limite = datetime.strptime(data_limite, "%d-%m-%Y").date()
        elif isinstance(data_limite, datetime):
            data_limite = data_limite.date()
        elif not isinstance(data_limite, date):
            raise TypeError("data_limite deve ser date, datetime ou string no formato DD-MM-AAAA")

        self._id = id
        self._titulo = titulo
        self._descricao = descricao
        self._data_limite = data_limite
        self._concluida = False  # Status inicial (não concluída)

    def concluir(self): # Método para marcar a conclusão da tarefa
        self._concluida = True
        self.touch() # Atualiza o timestamp de modificação

# Métodos GETTERS, permitem acessaar os dados encapsulados de forma segura
    def get_id(self):
        return self._id
    
    def get_titulo(self):
        return self._titulo
    
    def get_descricao(self):
        return self._descricao
    
    def get_data_limite(self):
        return self._data_limite  # <- RETORNA um date
    
    def esta_concluida(self):
        return self._concluida
    
    def __str__(self):
        status = "✅" if self._concluida else "❌"
        data_formatada = self._data_limite.strftime("%d-%m-%Y") # formata a data limite como dia-mês-ano
        return f"[{status}] {self._id} - {self._titulo} (até {data_formatada})"

    def set_titulo(self, novo_titulo: str): # Atualiza o título e registra data de modificação.
        self._titulo = novo_titulo
        self.touch()

    def set_descricao(self, nova_descricao: str): # Atualiza a descrição e registra data de modificação.
        self._descricao = nova_descricao
        self.touch()

    def set_data_limite(self, nova_data_limite: date): # Atualiza a data limite e registra data de modificação.
        self._data_limite = nova_data_limite
        self.touch()

    def get_data_limite_obj(self): # Retorna a data limite como objeto date (para comparação)
        if isinstance(self._data_limite, str):
            return datetime.strptime(self._data_limite, "%d-%m-%Y").date()
        return self._data_limite
