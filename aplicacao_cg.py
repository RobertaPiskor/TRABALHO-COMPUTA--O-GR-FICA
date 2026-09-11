import tkinter as tk
from viewport import ViewPoint
from formas_geometricas import FormasGeometricas
from janela_transformada import JanelaTransformacoes
from descritor_obj import DescritorOBJ

# ==============================
# CLASSE PRINCIPAL DA APLICAÇÃO
# ==============================

class AplicacaoCG:
    def __init__(self, root):
        self.root = root
        self.root.title("Computação Gráfica")
        self.viewport = ViewPoint(600, 600)
        self.elementosGeometricos = []
        self.criar_interface()
        self.carregar_dados_iniciais()

    def criar_interface(self):
        self.canvas = tk.Canvas(self.root, width=600, height=600, background="white", highlightthickness=0, bd=0)
        self.canvas.grid(row=0, column=1)
    
    # =================================
    # INTERFACE EM SI (BOTÕES E LISTA)
    # =================================

    # =========================================================
    # Botões zooms, up, down, left e right e rotacionar windows

        self.frame_botoes = tk.Frame(self.root, padx=10, pady=10)
        self.frame_botoes.grid(row=0, column=0, sticky="n")

        tk.Label(self.frame_botoes, text="Rotação Window (°):", font=("Times New Roman", 10, "bold")).pack(anchor="w", pady=(10, 0))
        frame_rotacao_window = tk.Frame(self.frame_botoes)
        frame_rotacao_window.pack(fill="x", pady=2)
        self.entrada_angulo_window = tk.Entry(frame_rotacao_window, width=8)
        self.entrada_angulo_window.pack(side="left", padx=(0, 5))
        tk.Button(frame_rotacao_window, text="Rotacionar", font=("Times New Roman", 9, "bold"), command=self.rotacionar_window).pack(side="left", fill="x", expand=True)


        tk.Button(self.frame_botoes, text="Zoom in", font=("Times New Roman", 10, "bold"), command=self.zoomIn).pack(fill="x", pady=2)
        tk.Button(self.frame_botoes, text="Zoom out", font=("Times New Roman", 10, "bold"), command=self.zoomOut).pack(fill="x", pady=2)
        tk.Button(self.frame_botoes, text="Left", font=("Times New Roman", 10, "bold"), command=self.left).pack(fill="x", pady=2)
        tk.Button(self.frame_botoes, text="Right", font=("Times New Roman", 10, "bold"), command=self.right).pack(fill="x", pady=2)
        tk.Button(self.frame_botoes, text="Up", font=("Times New Roman", 10, "bold"), command=self.up).pack(fill="x", pady=2)
        tk.Button(self.frame_botoes, text="Down", font=("Times New Roman", 10, "bold"), command=self.down).pack(fill="x", pady=2)

        tk.Label(self.frame_botoes, text="").pack(pady=5)

    # ==============================================================================================
    # Adicionar novas figuras (nome da figura - LINHA1) (pontos que nescessitam) (botão para enviar)

        tk.Label(self.frame_botoes, text="Nome da forma:", font=("Times New Roman", 10, "bold")).pack(anchor="w", pady=(10, 0))
        self.entrada_nome = tk.Entry(self.frame_botoes, width=20)
        self.entrada_nome.pack(fill="x", pady=2)

        tk.Label(self.frame_botoes, text="Pontos da forma ex:(x1,y1),(x2,y2)", font=("Times New Roman", 10, "bold")).pack(anchor="w", pady=(5, 0))
        self.entrada_pontos = tk.Entry(self.frame_botoes, width=20)
        self.entrada_pontos.pack(fill="x", pady=2)

        tk.Label(self.frame_botoes, text="Cor (opcional):", font=("Times New Roman", 10, "bold")).pack(anchor="w", pady=(5, 0))
        self.entrada_cor = tk.Entry(self.frame_botoes, width=20)
        self.entrada_cor.pack(fill="x", pady=2)

        tk.Button(self.frame_botoes, text="Adicionar Forma", font=("Times New Roman", 10, "bold"), command=self.forma_vinda_da_interface).pack(fill="x", pady=5)

    # ==============================
    # Lista das figuras geométricas

        self.frame_lista = tk.Frame(self.root)
        self.frame_lista.grid(row=0, column=2, sticky="ns", padx=5)

        tk.Label(self.frame_lista, text="Objetos na Tela", font=("Times New Roman", 10, "bold")).pack(anchor="w")

        self.lista_elementos = tk.Listbox(self.frame_lista, width=30, height=35)
        self.lista_elementos.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.frame_lista, orient="vertical", command=self.lista_elementos.yview) # se passou a tela roda para baixo
        scrollbar.pack(side="right", fill="y")
        self.lista_elementos.config(yscrollcommand=scrollbar.set)

        self.lista_elementos.bind("<<ListboxSelect>>", self.ao_selecionar_elemento) # as formas que estarão dentro 

    # ==================================
    # Para não começar sem nada na tela

    def carregar_dados_iniciais(self):
        descritor = DescritorOBJ()
        dados_lidos = descritor.ler_arquivo("formas_aplicacao_cg.obj")            
        self.elementosGeometricos = []
        for item in dados_lidos:
            forma = FormasGeometricas(item[0], item[1], item[2], item[3])
            self.elementosGeometricos.append(forma)
            self.lista_elementos.insert(tk.END, forma.nome)
            if self.elementosGeometricos:
                self.redraw()
                
    # =================================================================
    # Coloca as figuras na tela (deleta tudo e coloca da forma correta)

    def redraw(self):
        self.canvas.delete("all") 
        for elemento in self.elementosGeometricos:
            elemento.adiconar_na_tela(self.canvas, self.viewport)

    def salvar_formas_em_obj(self):
        with open("formas_aplicacao_cg.obj", "w", encoding="utf-8") as arquivo:
            descritor = DescritorOBJ(arquivo)
            for elemento in self.elementosGeometricos:
                descritor.escrever_arquivo(elemento)
    # ==================================================================================================================
    # Quando se aperta um botão vem para cá e depois vai ser feito o que se deve (no sentido de dar zoom e essas coisas)

    def rotacionar_window(self):
        angulo = float(self.entrada_angulo_window.get().strip())
        self.viewport.rotacao_window(angulo) 
        self.redraw()   
        self.entrada_angulo_window.delete(0, tk.END)      

    def zoomIn(self):
        self.viewport.zoomIn()
        self.redraw()

    def zoomOut(self):
        self.viewport.zoomOut()
        self.redraw()

    def right(self):
        self.viewport.right()
        self.redraw()

    def left(self):
        self.viewport.left()
        self.redraw()

    def down(self):
        self.viewport.down()
        self.redraw()

    def up(self):
        self.viewport.up()
        self.redraw()

    # ==============================================
    # Vai abrir outra tela para mexer nos elementos

    def ao_selecionar_elemento(self, event):
        selecao = self.lista_elementos.curselection()
        if selecao:
            indice = selecao[0]
            self.lista_elementos.selection_clear(0, tk.END)
            elemento_selecionado = self.elementosGeometricos[indice]
            JanelaTransformacoes(self.root, elemento_selecionado, self)
            self.salvar_formas_em_obj()

    # =============================================================================
    # Entra os pontos e criamos o objeto novo, linha, ponto ou polígonos (inserido)

    def processar_entrada(self, nome: str, pontos_string: str, cor: str = None):
        pontos = list(eval(f"[{pontos_string}]"))
        qtd_pontos = len(pontos)
        forma = None
        cor_hexadecimal = None
        if cor and cor.strip() != "":
            cor_rgb = self.canvas.winfo_rgb(cor)
            red_cor = cor_rgb[0] // 256
            green_cor = cor_rgb[1] // 256
            blue_cor = cor_rgb[2] // 256
            cor_hexadecimal = f"#{red_cor:02x}{green_cor:02x}{blue_cor:02x}"
        if qtd_pontos == 1:
            tipo = "ponto"
            pontos_formatados = [(float(pontos[0][0]), float(pontos[0][1]))]
        elif qtd_pontos == 2:
            tipo = "linha"
            (x1, y1), (x2, y2) = pontos
            pontos_formatados = [(float(x1), float(y1)), (float(x2), float(y2))]
        elif qtd_pontos > 2:
            tipo = "wireframe" 
            pontos_formatados = [(float(x), float(y)) for x, y in pontos]
        else:
            print("ERRO!")
        forma = FormasGeometricas(nome, tipo, pontos_formatados, cor_hexadecimal)
        if forma is not None:
            self.elementosGeometricos.append(forma)
            self.lista_elementos.insert(tk.END, forma.nome)
            self.salvar_formas_em_obj()
            self.redraw()

    # ===============================================
    # Entrada para inserir a nova forma está correta?

    def forma_vinda_da_interface(self):
        nome = self.entrada_nome.get().strip()
        pontos_string = self.entrada_pontos.get().strip()
        cor = self.entrada_cor.get().strip() or None

        if nome and pontos_string:
            self.processar_entrada(nome, pontos_string, cor)

        # Enviou? Então tira tudo que estava escrito antes
        self.entrada_nome.delete(0, tk.END)
        self.entrada_pontos.delete(0, tk.END)
        self.entrada_cor.delete(0, tk.END)