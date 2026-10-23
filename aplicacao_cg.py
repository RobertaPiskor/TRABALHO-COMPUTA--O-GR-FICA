import tkinter as tk
from viewport import ViewPoint
from formas_geometricas import FormasGeometricas, ObjetoWindow
from curvas_formas_2d import FormaCurva
from janela_transformada import JanelaTransformacoes
from descritor_obj import DescritorOBJ
from tkinter import filedialog, messagebox

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
        # 1. Botão para abrir janela de Curvas
        self.btn_abrir_curvas = tk.Button(self.frame_botoes, text="Adicionar Curvas (Bézier/B-Spline)", font=("Times New Roman", 10, "bold"), command=self.abrir_janela_curvas)
        self.btn_abrir_curvas.pack(fill="x", pady=5)

        # =======================================
        # 2. Botão para abrir janela de Formas 3D
        self.btn_abrir_formas = tk.Button(self.frame_botoes, text="Adicionar Formas 3D", font=("Times New Roman", 10, "bold"), command=self.abrir_janela_formas)
        self.btn_abrir_formas.pack(fill="x", pady=5)

        # ========================
        # 3. Algoritmo de Clipping
        self.grupo_clipping = tk.LabelFrame(self.frame_botoes, text="Algoritmo de Clipping", font=("Times New Roman", 10, "bold"), padx=10, pady=10)
        self.grupo_clipping.pack(fill="x", pady=5)

        self.escolhe_clipping = tk.StringVar(value="Cohen-Sutherland")
        tk.Radiobutton(self.grupo_clipping, text="Cohen-Sutherland", variable=self.escolhe_clipping, value="Cohen-Sutherland", font=("Times New Roman", 10, "bold"), command=self.mudar_clipping).pack(anchor="w")
        tk.Radiobutton(self.grupo_clipping, text="Liang-Barsky", variable=self.escolhe_clipping, value="Liang-Barsky", font=("Times New Roman", 10, "bold"), command=self.mudar_clipping).pack(anchor="w")

        # =======================================
        # 4. Botões de Importação e Exportação
        self.grupo_arquivos = tk.LabelFrame(self.frame_botoes, text="Arquivos (.obj)", font=("Times New Roman", 10, "bold"), padx=10, pady=5)
        self.grupo_arquivos.pack(fill="x", pady=5)
        
        tk.Button(self.grupo_arquivos, text="Importar OBJ", font=("Times New Roman", 9), command=self.importar_obj).pack(fill="x", pady=2)
        tk.Button(self.grupo_arquivos, text="Exportar OBJ", font=("Times New Roman", 9), command=self.exportar_obj).pack(fill="x", pady=2)

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

        # =========================
        # 7. Botões de perspectiva
        self.vd = tk.DoubleVar(value=self.viewport.d)

        self.grupo_perspectiva = tk.LabelFrame(self.frame_botoes, text="Tipo de Projeção", font=("Times New Roman", 10, "bold"), padx=10, pady=10)
        self.grupo_perspectiva.pack(fill="x", pady=5)

        # Novos botões de seleção criados
        self.var_projecao = tk.StringVar(value="ortogonal")
        tk.Radiobutton(self.grupo_perspectiva, text="Ortogonal", variable=self.var_projecao, value="ortogonal", font=("Times New Roman", 10, "bold"), command=self.mudar_projecao).pack(anchor="w")
        tk.Radiobutton(self.grupo_perspectiva, text="Perspectiva", variable=self.var_projecao, value="perspectiva", font=("Times New Roman", 10, "bold"), command=self.mudar_projecao).pack(anchor="w")

        tk.Label(self.grupo_perspectiva, text="Distância do COP ao plano (d)", font=("Times New Roman", 9)).pack(anchor="w", pady=(5,0))
        tk.Scale(self.grupo_perspectiva, from_=100, to=4000, resolution=10, orient="horizontal",variable=self.vd, length=220,command=lambda valor: self.mudar_perspectiva()).pack(fill="x")


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
        with open("cenario_modificado.obj", "w", encoding="utf-8") as arquivo:
            descritor = DescritorOBJ(arquivo)
            for elemento in self.elementosGeometricos:
                if getattr(elemento, 'tipo', '') != "curva" and getattr(elemento, 'tipo', '') != "CAMERA":
                    descritor.escrever_arquivo(elemento)
            descritor.gerar_arquivo_mtl("cores.mtl")
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

    def mudar_perspectiva(self):
        novo_d = self.vd.get()        
        self.viewport.d = novo_d
        self.redraw()

    def mudar_projecao(self):
        self.viewport.observacao = self.var_projecao.get()
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

    def importar_obj(self):
        caminho_arquivo = filedialog.askopenfilename(
            title="Importar Arquivo OBJ",
            filetypes=[("Arquivos OBJ", "*.obj"), ("Todos os Arquivos", "*.*")]
        )
        if caminho_arquivo:
            descritor = DescritorOBJ()
            dados_lidos = descritor.ler_arquivo(caminho_arquivo)
            
            if not dados_lidos:
                messagebox.showwarning("Aviso", "Não foi possível carregar as formas ou o arquivo está vazio.")
                return
                
            for item in dados_lidos:
                forma = FormasGeometricas(item[0], item[1], item[2], item[3], item[4])
                self.elementosGeometricos.append(forma)
                self.lista_elementos.insert(tk.END, forma.nome)
            
            self.redraw()
            messagebox.showinfo("Sucesso", "Arquivo OBJ importado com sucesso!")

    def exportar_obj(self):
        caminho_arquivo = filedialog.asksaveasfilename(
            title="Exportar Arquivo OBJ",
            defaultextension=".obj",
            filetypes=[("Arquivos OBJ", "*.obj")]
        )
        import os
        if caminho_arquivo:
            caminho_mtl = caminho_arquivo.replace(".obj", ".mtl")
            nome_mtl = os.path.basename(caminho_mtl)
            
            with open(caminho_arquivo, "w", encoding="utf-8") as arquivo:
                descritor = DescritorOBJ(arquivo, nome_mtl=nome_mtl)
                for elemento in self.elementosGeometricos:
                    if getattr(elemento, 'tipo', '') not in ["curva", "CAMERA"]:
                        descritor.escrever_arquivo(elemento)
                
                descritor.gerar_arquivo_mtl(caminho_mtl)
                
            messagebox.showinfo("Sucesso", "Cenário exportado com sucesso!")


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

    # ==============================================
    # Janela Pop-up para adicionar Curvas
    def abrir_janela_curvas(self):
        janela_curvas = tk.Toplevel(self.root)
        janela_curvas.title("ADICIONAR CURVA")
        janela_curvas.geometry("273x300")
        janela_curvas.grab_set() 
        
        grupo = tk.Frame(janela_curvas, padx=15, pady=15)
        grupo.pack(fill="both", expand=True)

        self.var_tipo_curva = tk.StringVar(value="bezier")
        tk.Radiobutton(grupo, text="Bézier", variable=self.var_tipo_curva, value="bezier", font=("Times New Roman", 9)).pack(anchor="w")
        tk.Radiobutton(grupo, text="B-Spline (Forward Diff)", variable=self.var_tipo_curva, value="bspline", font=("Times New Roman", 9)).pack(anchor="w")

        tk.Label(grupo, text="Nome da curva:", font=("Times New Roman", 9)).pack(anchor="w", pady=(10, 0))
        self.entrada_nome_curva = tk.Entry(grupo, width=30)
        self.entrada_nome_curva.pack(fill="x", pady=2)

        tk.Label(grupo, text="Pontos ex: (x,y,z)... (Min: 4):", font=("Times New Roman", 9)).pack(anchor="w", pady=(5, 0))
        self.entrada_pontos_curva = tk.Entry(grupo, width=30)
        self.entrada_pontos_curva.pack(fill="x", pady=2)

        tk.Label(grupo, text="Cor hexadecimal/nome (opcional):", font=("Times New Roman", 9)).pack(anchor="w", pady=(5, 0))
        self.entrada_cor_curva = tk.Entry(grupo, width=30)
        self.entrada_cor_curva.pack(fill="x", pady=2)

        # Chama a função de adicionar a curva e depois destrói a janelinha
        tk.Button(grupo, text="Adicionar Curva", font=("Times New Roman", 9, "bold"), command=lambda: [self.forma_vinda_da_interface_curva(), janela_curvas.destroy()]).pack(fill="x", pady=15)

    # ==============================================
    # Janela Pop-up para adicionar Formas 3D
    def abrir_janela_formas(self):
        janela_formas = tk.Toplevel(self.root)
        janela_formas.title("Adicionar Forma 3D")
        janela_formas.geometry("350x380")
        janela_formas.grab_set() 
        
        grupo = tk.Frame(janela_formas, padx=15, pady=15)
        grupo.pack(fill="both", expand=True)

        tk.Label(grupo, text="Nome da forma:", font=("Times New Roman", 9)).pack(anchor="w")
        self.entrada_nome = tk.Entry(grupo, width=30)
        self.entrada_nome.pack(fill="x", pady=2)

        tk.Label(grupo, text="Vértices (x,y,z),... :", font=("Times New Roman", 9)).pack(anchor="w", pady=(5, 0))
        self.entrada_pontos = tk.Entry(grupo, width=30)
        self.entrada_pontos.pack(fill="x", pady=2)

        tk.Label(grupo, text="Faces (índices) ex: [0,1,2],[1,2,3]:", font=("Times New Roman", 9)).pack(anchor="w", pady=(5, 0))
        self.entrada_conexoes = tk.Entry(grupo, width=30)
        self.entrada_conexoes.pack(fill="x", pady=2)

        tk.Label(grupo, text="Cor hexadecimal ou nome (opcional):", font=("Times New Roman", 9)).pack(anchor="w", pady=(5, 0))
        self.entrada_cor = tk.Entry(grupo, width=30)
        self.entrada_cor.pack(fill="x", pady=2)

        self.var_preenchido = tk.BooleanVar(value=False) 
        tk.Radiobutton(grupo, text="Polígono preenchido", variable=self.var_preenchido, value=True, font=("Times New Roman", 9)).pack(anchor="w")
        tk.Radiobutton(grupo, text="Wireframe (Arame)", variable=self.var_preenchido, value=False, font=("Times New Roman", 9)).pack(anchor="w")
        
        tk.Button(grupo, text="Adicionar", font=("Times New Roman", 9, "bold"), command=lambda: [self.forma_vinda_da_interface(), janela_formas.destroy()]).pack(fill="x", pady=15)