import tkinter as tk
from aplicacao_cg import AplicacaoCG
from janela_transformada import JanelaTransformacoes

# ==============================
# EXECUÇÃO DA APLICAÇÃO
# ==============================

if __name__ == "__main__":
    root = tk.Tk()
    app = AplicacaoCG(root)
    root.mainloop()