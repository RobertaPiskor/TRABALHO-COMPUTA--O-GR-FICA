import tkinter as tk
from viewport import ViewPoint
from formas_geometricas import FormasGeometricas, ObjetoWindow
from curvas_formas_2d import FormaCurva
from janela_transformada import JanelaTransformacoes
from descritor_obj import DescritorOBJ

# ==============================
# CLASSE PRINCIPAL DA APLICAÇÃO
# ==============================

class AplicacaoCG:
    def __init__(self, root):
        self.root = root
        self.root.title("SISTEMA GRÁFICO INTERATIVO 3D")
        self.viewport = ViewPoint(600, 600)        
        self.objeto_camera = ObjetoWindow(self.viewport)
        self.elementosGeometricos = [self.objeto_camera] 
        self.criar_interface()
        self.lista_elementos.insert(tk.END, self.objeto_camera.nome)
        self.carregar_dados_iniciais()

    # =============================================
    # IA -> foi usado ia para ajustar os botões e a lista (questão como por exemplo local onde ficaria, centralização, ...). O motivo foi estético

    def criar_interface(self):
        self.canvas = tk.Canvas(self.root, width=600, height=600, background="white", highlightthickness=0, bd=0)
        self.canvas.grid(row=0, column=1, padx=10, pady=10)
        
        # ==============================================
        # PAINEL ESQUERDO: criar e configurar
        # ==============================================
        
        self.frame_botoes = tk.Frame(self.root, padx=10, pady=10)
        self.frame_botoes.grid(row=0, column=0, sticky="n")

        # =========================
        # 1. Adicionar Curva Bezier ou B-Spline
        self.grupo_curvas = tk.LabelFrame(self.frame_botoes, text="Adicionar Curvas", font=("Times New Roman", 10, "bold"), padx=10, pady=10)
        self.grupo_curvas.pack(fill="x", pady=5)

        self.var_tipo_curva = tk.StringVar(value="bezier")
        tk.Radiobutton(self.grupo_curvas, text="Bézier", variable=self.var_tipo_curva, value="bezier", font=("Times New Roman", 9)).pack(anchor="w")
        tk.Radiobutton(self.grupo_curvas, text="B-Spline (Forward Diff)", variable=self.var_tipo_curva, value="bspline", font=("Times New Roman", 9)).pack(anchor="w")

        tk.Label(self.grupo_curvas, text="Nome da curva:", font=("Times New Roman", 9)).pack(anchor="w", pady=(5, 0))
        self.entrada_nome_curva = tk.Entry(self.grupo_curvas, width=20)
        self.entrada_nome_curva.pack(fill="x", pady=2)

        tk.Label(self.grupo_curvas, text="Pontos ex: (x,y,z)... (Min: 4):", font=("Times New Roman", 9)).pack(anchor="w", pady=(5, 0))
        self.entrada_pontos_curva = tk.Entry(self.grupo_curvas, width=20)
        self.entrada_pontos_curva.pack(fill="x", pady=2)

        tk.Label(self.grupo_curvas, text="Cor hexadecimal/nome (opcional):", font=("Times New Roman", 9)).pack(anchor="w", pady=(5, 0))
        self.entrada_cor_curva = tk.Entry(self.grupo_curvas, width=20)
        self.entrada_cor_curva.pack(fill="x", pady=2)

        tk.Button(self.grupo_curvas, text="Adicionar Curva", font=("Times New Roman", 9, "bold"), command=self.forma_vinda_da_interface_curva).pack(fill="x", pady=5)

        # ========================
        # 2. Adicionar Formas Base
        self.grupo_formas = tk.LabelFrame(self.frame_botoes, text="Adicionar Formas 3D", font=("Times New Roman", 10, "bold"), padx=10, pady=10)
        self.grupo_formas.pack(fill="x", pady=5)

        tk.Label(self.grupo_formas, text="Nome da forma:", font=("Times New Roman", 9)).pack(anchor="w")
        self.entrada_nome = tk.Entry(self.grupo_formas, width=20)
        self.entrada_nome.pack(fill="x", pady=2)

        tk.Label(self.grupo_formas, text="Vértices (x,y,z),... :", font=("Times New Roman", 9)).pack(anchor="w", pady=(5, 0))
        self.entrada_pontos = tk.Entry(self.grupo_formas, width=20)
        self.entrada_pontos.pack(fill="x", pady=2)

        tk.Label(self.grupo_formas, text="Faces (índices) ex: [0,1,2],[1,2,3]:", font=("Times New Roman", 9)).pack(anchor="w", pady=(5, 0))
        self.entrada_conexoes = tk.Entry(self.grupo_formas, width=20)
        self.entrada_conexoes.pack(fill="x", pady=2)

        tk.Label(self.grupo_formas, text="Cor hexadecimal ou nome (opcional):", font=("Times New Roman", 9)).pack(anchor="w", pady=(5, 0))
        self.entrada_cor = tk.Entry(self.grupo_formas, width=20)
        self.entrada_cor.pack(fill="x", pady=2)

        self.var_preenchido = tk.BooleanVar(value=False) 
        tk.Radiobutton(self.grupo_formas, text="Polígono preenchido", variable=self.var_preenchido, value=True, font=("Times New Roman", 9)).pack(anchor="w")
        tk.Radiobutton(self.grupo_formas, text="Wireframe (Arame)", variable=self.var_preenchido, value=False, font=("Times New Roman", 9)).pack(anchor="w")
        tk.Button(self.grupo_formas, text="Adicionar", font=("Times New Roman", 9, "bold"), command=self.forma_vinda_da_interface).pack(fill="x", pady=5)
        
        # ========================
        # 3. Algoritmo de Clipping
        self.grupo_clipping = tk.LabelFrame(self.frame_botoes, text="Algoritmo de Clipping", font=("Times New Roman", 10, "bold"), padx=10, pady=10)
        self.grupo_clipping.pack(fill="x", pady=5)

        self.escolhe_clipping = tk.StringVar(value="Cohen-Sutherland")
        tk.Radiobutton(self.grupo_clipping, text="Cohen-Sutherland", variable=self.escolhe_clipping, value="Cohen-Sutherland", font=("Times New Roman", 10, "bold"), command=self.mudar_clipping).pack(anchor="w")
        tk.Radiobutton(self.grupo_clipping, text="Liang-Barsky", variable=self.escolhe_clipping, value="Liang-Barsky", font=("Times New Roman", 10, "bold"), command=self.mudar_clipping).pack(anchor="w")

        # ==============================================
        # PAINEL DIREITO: (Lista e Navegação)
        # ==============================================
        self.frame_lista = tk.Frame(self.root)
        self.frame_lista.grid(row=0, column=2, sticky="ns", padx=5)

        # ================================
        # 4. Lista das figuras geométricas
        tk.Label(self.frame_lista, text="Objetos na Tela", font=("Times New Roman", 10, "bold")).pack(anchor="w")
        
        self.lista_elementos = tk.Listbox(self.frame_lista, width=40, height=22) 
        self.lista_elementos.pack(side="top", fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.frame_lista, orient="vertical", command=self.lista_elementos.yview) 
        scrollbar.pack(side="right", fill="y")
        self.lista_elementos.config(yscrollcommand=scrollbar.set)
        self.lista_elementos.bind("<<ListboxSelect>>", self.ao_selecionar_elemento)

        # ===============================================
        # 5. Navegação da Window (Anexado ao frame_lista)
        self.grupo_movimento = tk.LabelFrame(self.frame_lista, text="Navegação da Câmera", font=("Times New Roman", 10, "bold"), padx=10, pady=10)
        self.grupo_movimento.pack(side="bottom", fill="x", pady=10)

        frame_botoes_nav = tk.Frame(self.grupo_movimento)
        frame_botoes_nav.pack(fill="x", pady=5)
        
        # ============================================================================
        # 6. Botões de navegação organizados com grid interno para ficarem mais compactos
        tk.Button(frame_botoes_nav, text="Zoom in", font=("Times New Roman", 9), command=self.zoomIn, width=15).grid(row=0, column=0, padx=2, pady=2)
        tk.Button(frame_botoes_nav, text="Zoom out", font=("Times New Roman", 9), command=self.zoomOut, width=15).grid(row=0, column=1, padx=2, pady=2)
        
        tk.Button(frame_botoes_nav, text="Esquerda ", font=("Times New Roman", 9), command=self.left, width=15).grid(row=1, column=0, padx=2, pady=2)
        tk.Button(frame_botoes_nav, text="Direita", font=("Times New Roman", 9), command=self.right, width=15).grid(row=1, column=1, padx=2, pady=2)
        
        tk.Button(frame_botoes_nav, text="Cima", font=("Times New Roman", 9), command=self.up, width=15).grid(row=2, column=0, padx=2, pady=2)
        tk.Button(frame_botoes_nav, text="Baixo", font=("Times New Roman", 9), command=self.down, width=15).grid(row=2, column=1, padx=2, pady=2)

    # ==================================
    # Para não começar sem nada na tela

    def carregar_dados_iniciais(self):
        descritor = DescritorOBJ()
        dados_lidos = descritor.ler_arquivo("formas_aplicacao_cg.obj")            
        for item in dados_lidos:
            forma = FormasGeometricas(item[0], item[1], item[2], item[3], item[4])
            self.elementosGeometricos.append(forma)
            self.lista_elementos.insert(tk.END, forma.nome)
        if len(self.elementosGeometricos) > 1:
            self.redraw()

    # =================================================================
    # Coloca as figuras na tela (deleta tudo e coloca da forma correta)

    def redraw(self):
        self.canvas.delete("all") 
        for elemento in self.elementosGeometricos:
            if getattr(elemento, 'tipo', '') != "CAMERA":
                elemento.adiconar_na_tela(self.canvas, self.viewport)
        self.canvas.create_rectangle(10, 10, 590, 590, outline="#000000", width=1, dash=(40,15))

    def salvar_formas_em_obj(self):
        with open("formas_aplicacao_cg.obj", "w", encoding="utf-8") as arquivo:
            descritor = DescritorOBJ(arquivo)
            for elemento in self.elementosGeometricos:
                if getattr(elemento, 'tipo', '') != "curva" and getattr(elemento, 'tipo', '') != "CAMERA":
                    descritor.escrever_arquivo(elemento)

    # ==================================================================================================================
    # Quando se aperta um botão vem para cá e depois vai ser feito o que se deve (no sentido de dar zoom e essas coisas)

    def zoomIn(self): self.viewport.zoomIn(); self.redraw()
    def zoomOut(self): self.viewport.zoomOut(); self.redraw()
    def right(self): self.viewport.right(); self.redraw()
    def left(self): self.viewport.left(); self.redraw()
    def down(self): self.viewport.down(); self.redraw()
    def up(self): self.viewport.up(); self.redraw()

    def mudar_clipping(self):
        self.viewport.clipping = self.escolhe_clipping.get()
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
            if getattr(elemento_selecionado, 'tipo', '') not in ["curva", "CAMERA"]:
                self.salvar_formas_em_obj()

    # =============================================================================
    # Entra os pontos e criamos o objeto novo, linha, ponto ou polígonos (inserido)
    def processar_entrada(self, nome: str, pontos_string: str, conexoes_string: str, cor: str = None, preenchido: bool = False):
        pontos = list(eval(f"[{pontos_string}]"))
        qtd_pontos = len(pontos)
        
        pontos_formatados = []
        for p in pontos:
            if len(p) == 2: pontos_formatados.append((float(p[0]), float(p[1]), 0.0))
            elif len(p) >= 3: pontos_formatados.append((float(p[0]), float(p[1]), float(p[2])))

        conexoes = []
        if conexoes_string: conexoes = list(eval(f"[{conexoes_string}]"))

        cor_hexadecimal = None
        if cor and cor.strip() != "":
            cor_rgb = self.canvas.winfo_rgb(cor)
            cor_hexadecimal = f"#{cor_rgb[0]//256:02x}{cor_rgb[1]//256:02x}{cor_rgb[2]//256:02x}"
            
        if qtd_pontos == 1: tipo = "ponto"
        elif qtd_pontos == 2: tipo = "linha"
        elif qtd_pontos > 2:
            if preenchido: tipo = "poligono_preenchido"
            else: tipo = "wireframe"
        else:
            print("ERRO!")
            return
            
        forma = FormasGeometricas(nome, tipo, pontos_formatados, conexoes, cor_hexadecimal)
        self.elementosGeometricos.append(forma)
        self.lista_elementos.insert(tk.END, forma.nome)
        self.salvar_formas_em_obj()
        self.redraw()

    # ===============================================
    # Entrada para inserir a nova forma está correta?

    def forma_vinda_da_interface(self):
        nome = self.entrada_nome.get().strip()
        pontos_string = self.entrada_pontos.get().strip()
        conexoes_string = self.entrada_conexoes.get().strip()
        cor = self.entrada_cor.get().strip() or None
        escolha_preenchido = self.var_preenchido.get()

        if nome and pontos_string:
            self.processar_entrada(nome, pontos_string, conexoes_string, cor, escolha_preenchido)

        self.entrada_nome.delete(0, tk.END)
        self.entrada_pontos.delete(0, tk.END)
        self.entrada_conexoes.delete(0, tk.END)
        self.entrada_cor.delete(0, tk.END)
        self.var_preenchido.set(False)

    def processar_entrada_curva(self, nome: str, pontos_string: str, cor: str = None, tipo_curva: str = "bezier"):
        pontos = list(eval(f"[{pontos_string}]"))
        
        if len(pontos) < 4: return 

        pontos_formatados = []
        for p in pontos:
            if len(p) == 2: pontos_formatados.append((float(p[0]), float(p[1]), 0.0))
            elif len(p) >= 3: pontos_formatados.append((float(p[0]), float(p[1]), float(p[2])))

        cor_hexadecimal = None
        if cor and cor.strip() != "":
            cor_rgb = self.canvas.winfo_rgb(cor)
            cor_hexadecimal = f"#{cor_rgb[0]//256:02x}{cor_rgb[1]//256:02x}{cor_rgb[2]//256:02x}"
            
        forma = FormaCurva(nome, pontos_formatados, cor_hexadecimal, tipo_curva)
        self.elementosGeometricos.append(forma)
        self.lista_elementos.insert(tk.END, forma.nome)
        self.redraw()

    # ================================
    # Entrou algo de curvas? PROCESSA!
    
    def forma_vinda_da_interface_curva(self):
        nome = self.entrada_nome_curva.get().strip()
        pontos_string = self.entrada_pontos_curva.get().strip()
        cor = self.entrada_cor_curva.get().strip() or None
        tipo_curva = self.var_tipo_curva.get()

        if nome and pontos_string:
            self.processar_entrada_curva(nome, pontos_string, cor, tipo_curva)

        self.entrada_nome_curva.delete(0, tk.END)
        self.entrada_pontos_curva.delete(0, tk.END)
        self.entrada_cor_curva.delete(0, tk.END)