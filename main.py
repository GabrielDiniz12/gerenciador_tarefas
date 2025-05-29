# main.py
from tkinter import Tk
from package.gui import AplicacaoTarefas

if __name__ == "__main__":
    raiz = Tk()
    app = AplicacaoTarefas(raiz)
    raiz.mainloop()
