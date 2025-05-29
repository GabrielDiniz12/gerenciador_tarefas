import customtkinter as ctk
from tkinter import messagebox, END
from tkinter import Listbox, SINGLE
from package.models import Tarefa
from package.controllers import GerenciadorTarefas
from package.persistence import RepositorioTarefas
from datetime import date, datetime

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class AplicacaoTarefas:
    def __init__(self, raiz):
        self.gerenciador = GerenciadorTarefas()
        self.raiz = raiz
        self.raiz.title("Gerenciador de Tarefas")
        self.raiz.geometry("700x700")
        self.raiz.resizable(False, False)
        self.tarefa_em_edicao = None
        self.iniciar()

        self.frame_principal = ctk.CTkFrame(self.raiz)
        self.frame_principal.pack(pady=10, padx=10, fill="both", expand=True)

        # LISTBOX COM FUNDO ESCURO E TEXTO CLARO
        self.lista = Listbox(self.frame_principal, selectmode=SINGLE, height=10, width=100)
        self.lista.config(bg="#2b2b2b", fg="white", selectbackground="#4a90e2")
        self.lista.pack(pady=10)

        self.entrada_titulo = ctk.CTkEntry(self.frame_principal, placeholder_text="Título da tarefa", width=400)
        self.entrada_titulo.pack(pady=5)

        self.entrada_desc = ctk.CTkEntry(self.frame_principal, placeholder_text="Descrição", width=400)
        self.entrada_desc.pack(pady=5)

        self.entrada_data = ctk.CTkEntry(self.frame_principal, placeholder_text="Data limite (DD-MM-AAAA)", width=400)
        self.entrada_data.pack(pady=5)

        self.verificacao = 0

        botoes = [
            ("Adicionar Tarefa", self.adicionar_tarefa),
            ("Editar Tarefa", self.editar_tarefa),
            ("Salvar Edição", self.salvar_edicao),
            ("Cancelar Edição", self.cancelar_edicao),
            ("Concluir Tarefa", self.concluir_tarefa),
            ("Remover Tarefa", self.remover_tarefa),
            ("Carregar Tarefas Salvas", self.carregar),
        ]

        for texto, comando in botoes:
            ctk.CTkButton(self.frame_principal, text=texto, command=comando, width=200).pack(pady=4)

    def atualizar_lista(self):
        self.lista.delete(0, END)
        for tarefa in self.gerenciador.listar_tarefas():
            self.lista.insert(END, str(tarefa))

    def obter_tarefa_selecionada(self):
        selecionados = self.lista.curselection()
        if not selecionados:
            raise Exception("Nenhuma tarefa selecionada.")
        return self.gerenciador.listar_tarefas()[selecionados[0]]

    def adicionar_tarefa(self):
        if self.verificacao == 0:
            try:
                titulo = self.entrada_titulo.get().strip()
                descricao = self.entrada_desc.get().strip()
                data_str = self.entrada_data.get().strip()

                if not titulo or not descricao or not data_str:
                    raise Exception("Todos os campos (Título, Descrição e Data) devem ser preenchidos.")

                data_limite = datetime.strptime(data_str, "%d-%m-%Y").date()

                tarefas = self.gerenciador.listar_tarefas()
                novo_id = max([t.get_id() for t in tarefas], default=0) + 1

                nova = Tarefa(novo_id, titulo, descricao, data_limite)
                self.gerenciador.add_tarefa(nova)
                self.atualizar_lista()
                messagebox.showinfo("Sucesso", "Tarefa adicionada com sucesso!")

                if date.today() > nova.get_data_limite_obj():
                    messagebox.showwarning("Atenção", "A tarefa já está com o prazo vencido.")

                self.salvar()
            except ValueError:
                messagebox.showerror("Erro", "Data inválida. Use o formato DD-MM-AAAA.")
            except Exception as e:
                messagebox.showerror("Erro", str(e))

    def concluir_tarefa(self):
        try:
            tarefa = self.obter_tarefa_selecionada()
            tarefa.concluir()
            self.atualizar_lista()
            self.salvar()
            messagebox.showinfo("Sucesso","Tarefa concluída com sucesso")
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def remover_tarefa(self):
        try:
            tarefa = self.obter_tarefa_selecionada()
            self.gerenciador.remover_tarefa(tarefa.get_id())
            self.atualizar_lista()
            self.salvar()
            self.verificacao = 0
            messagebox.showinfo("Tarefa removida","Tarefa removida com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", str(e))
            self.verificacao = 0

    def editar_tarefa(self):

        self.verificacao = 1

        try:
            tarefa = self.obter_tarefa_selecionada()
            messagebox.showinfo("Editar Tarefa", "Edite seus parâmetros iniciais.")
            self.tarefa_em_edicao = tarefa
            self.entrada_titulo.delete(0, END)
            self.entrada_titulo.insert(0, tarefa.get_titulo())
            self.entrada_desc.delete(0, END)
            self.entrada_desc.insert(0, tarefa.get_descricao())
            self.entrada_data.delete(0, END)
            self.entrada_data.insert(0, tarefa.get_data_limite().strftime("%d-%m-%Y"))

        except Exception as e:
            messagebox.showerror("Erro", str(e))
            self.verificacao = 0


    def salvar_edicao(self):
        try:
            if not self.tarefa_em_edicao:
                raise Exception("Nenhuma tarefa em edição.")

            novo_titulo = self.entrada_titulo.get()
            nova_desc = self.entrada_desc.get()
            nova_data = datetime.strptime(self.entrada_data.get(), "%d-%m-%Y").date()

            if self.gerenciador.editar_tarefa(self.tarefa_em_edicao.get_id(), novo_titulo, nova_desc, nova_data):
                self.atualizar_lista()
                if date.today() > nova_data:
                    messagebox.showwarning("Atenção", "A tarefa editada já está com o prazo vencido.")
                messagebox.showinfo("Sucesso", "Tarefa editada com sucesso.")
                self.salvar()
                self.verificacao = 0
            else:
                messagebox.showerror("Erro", "Tarefa não encontrada.")
                self.verificacao = 0
            self.tarefa_em_edicao = None

        except Exception as e:
            messagebox.showerror("Erro", str(e))
            self.verificacao = 0

    def cancelar_edicao(self):
        if self.tarefa_em_edicao is None:  # Check if there's no task being edited
            messagebox.showerror("Erro", "Nenhuma tarefa em edição!")
            return
            
        self.tarefa_em_edicao = None
        self.entrada_titulo.delete(0, END)
        self.entrada_desc.delete(0, END)
        self.entrada_data.delete(0, END)
        messagebox.showinfo("Edição Cancelada", "A edição da tarefa foi cancelada")
        self.verificacao = 0

    def salvar(self):
        try:
            RepositorioTarefas.salvar_em_arquivo(self.gerenciador.listar_tarefas(), "tarefas.json")
        except Exception as e:
            messagebox.showerror("Erro ao salvar", str(e))

    def carregar(self):
            try:
                tarefas = RepositorioTarefas.carregar_do_arquivo("tarefas.json")
                if not tarefas:
                    messagebox.showinfo("Nenhuma Tarefa", "Nenhuma tarefa salva.")
                    return

                self.gerenciador.substituir_tarefas(tarefas)
                self.atualizar_lista()
                messagebox.showinfo("Sucesso", "Tarefas carregadas!")  # Added success message

                atrasadas = self.gerenciador.tarefas_atrasadas()
                if atrasadas:
                    msg = "\n".join(f"- {t.get_titulo()} (vencida em {t.get_data_limite()})" for t in atrasadas)
                    messagebox.showwarning("Tarefas Atrasadas", f"As seguintes tarefas estão atrasadas:\n{msg}")
            except FileNotFoundError:
                messagebox.showinfo("Nenhuma Tarefa", "Nenhum arquivo de tarefas encontrado.")
            except Exception as e:
                messagebox.showerror("Erro ao carregar", str(e))

    def iniciar(self):
        try:
            tarefas = RepositorioTarefas.carregar_do_arquivo("tarefas.json")
            self.gerenciador.substituir_tarefas(tarefas)
            self.atualizar_lista()
        except Exception:
            pass
