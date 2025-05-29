# 📋 Projeto Livre de Orientação a Objetos - Gerenciador de Tarefas com Interface Gráfica (Python + CustomTkinter)

Este projeto é um gerenciador de tarefas simples, com interface gráfica desenvolvida em Python utilizando a biblioteca `customtkinter`. Ele permite adicionar, editar, remover e concluir tarefas, além de salvar e carregar as tarefas em um arquivo JSON.

---

## 📌 Motivação para a criação do projeto

Este projeto foi criado como parte do aprendizado na matéria Orientação a Objetos. Ele visa aplicar os seguintes conceitos fundamentais:

- Programação Orientada a Objetos (POO)
- Criação de Interfaces Gráficas (GUI)
- Persistência de dados com arquivos JSON
- Validação de entrada e tratamento de erros
- Organização e modularização de código com boas práticas

A ferramenta é útil para gerenciamento pessoal de tarefas.

---

## ✅ Casos de Uso

### 1. Adicionar nova tarefa
- O usuário informa o título, descrição e data limite.
- O sistema cria uma nova tarefa e a adiciona à lista.

### 2. Listar tarefas
- Exibe todas as tarefas cadastradas com informações relevantes.
- Permite visualizar tarefas pendentes e concluídas.

### 3. Editar tarefa
- Permite modificar o título, descrição ou data limite de uma tarefa existente.

### 4. Concluir tarefa
- Marca uma tarefa como concluída, sinalizando seu encerramento.

### 5. Remover tarefa
- Remove uma tarefa selecionada da lista.

### 6. Salvar tarefas
- As tarefas são salvas localmente em um arquivo `tarefas.json`.

### 7. Carregar tarefas
- Carrega tarefas previamente salvas ao iniciar o programa ou mediante solicitação.

### 8. Alertar sobre tarefas atrasadas
- O sistema avisa o usuário sobre tarefas cujo prazo já expirou.

---

## 🛠 Tecnologias Utilizadas

- Python 3.x
- [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter)
- Programação Orientada a Objetos
- Armazenamento em JSON

---

## 📂 Estrutura do Projeto

├── main.py
├── package/
│ ├── init.py
│ ├── models.py
│ ├── controllers.py
│ └── persistence.py
├── tarefas.json