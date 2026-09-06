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
        self.canvas = tk.Canvas(self.root, width=600, height=600, background="white") 
        self.canvas.grid(row=0, column=1)
    
    # =================================
    # INTERFACE EM SI (BOTÕES E LISTA)
    # =================================

    # =====================================
    # Botões zooms, up, down, left e right

        self.frame_botoes = tk.Frame(self.root, padx=10, pady=10)
        self.frame_botoes.grid(row=0, column=0, sticky="n")

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

        self.lista_elementos = tk.Listbox(self.frame_lista, width=20, height=35)
        self.lista_elementos.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(self.frame_lista, orient="vertical", command=self.lista_elementos.yview) # se passou a tela roda para baixo
        scrollbar.pack(side="right", fill="y")
        self.lista_elementos.config(yscrollcommand=scrollbar.set)

        self.lista_elementos.bind("<<ListboxSelect>>", self.ao_selecionar_elemento) # as formas que estarão dentro 

    # ==================================
    # Para não começar sem nada na tela

    def carregar_dados_iniciais(self):
        try:
            # Em vez de abrir o arquivo antes e passar para o descritor, 
            # passamos o caminho direto para o ler_arquivo que criamos agora pouco:
            descritor = DescritorOBJ()
            dados_lidos = descritor.ler_arquivo("formas_aplicacao_cg.obj")
            
            # Como a nova leitura retorna um dicionário com os dados, 
            # precisamos transformar em objetos FormasGeometricas reais:
            self.elementosGeometricos = []
            for item in dados_lidos:
                forma = FormasGeometricas(item["nome"], "wireframe", item["pontos"], item["cor"])
                self.elementosGeometricos.append(forma)
                self.lista_elementos.insert(tk.END, forma.nome)
                
            if self.elementosGeometricos:
                self.redraw()
                
        except FileNotFoundError:
            print("Arquivo .obj não encontrado. Criando dados iniciais...")
    # =================================================================
    # Coloca as figuras na tela (deleta tudo e coloca da forma correta)

    def redraw(self):
        self.canvas.delete("all") 
        for elemento in self.elementosGeometricos:
            elemento.adiconar_na_tela(self.canvas, self.viewport)

    def salvar_formas_em_obj(self):
        with open("formas_aplicacao_cg.obj", "w", encoding="utf-8") as arquivo:
            arquivo.write("# ARQUIVO FORMAS\n")
            descritor = DescritorOBJ(arquivo)
            for elemento in self.elementosGeometricos:
                descritor.escrever_arquivo(elemento)

    # ==================================================================================================================
    # Quando se aperta um botão vem para cá e depois vai ser feito o que se deve (no sentido de dar zoom e essas coisas)

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

    def processar_entrada(self, nome:str, pontos_string:str, cor:str):
        try:
            pontos = list(eval(f"[{pontos_string}]"))
            qtd_pontos = len(pontos)
            forma = None

    # =================================================================================================
    # Muda a cor (se for hexadecimal e nome da cor mesmo) para hexadecimal (* para colocar no arquivo)
            
            cor_rgb = self.canvas.winfo_rgb(cor)
            red_cor = cor_rgb[0] // 256
            green_cor = cor_rgb[1] // 256
            blue_cor = cor_rgb[2] // 256
            cor_hexadecimal = f"#{red_cor:02x}{green_cor:02x}{blue_cor:02x}"

            if qtd_pontos == 1: # ponto
                x, y = pontos[0]
                forma = (FormasGeometricas.drawPoint(nome, float(x), float(y), cor=cor_hexadecimal))
            elif qtd_pontos == 2: # reta
                (x1, y1), (x2, y2) = pontos
                forma = (FormasGeometricas.drawLine(nome, float(x1), float(y1), float(x2), float(y2), cor=cor_hexadecimal))
            elif qtd_pontos > 2: # polígono
                pontos_convertidos = [(float(x),float(y))for x, y in pontos]
                forma = (FormasGeometricas.drawWireframe(nome, pontos_convertidos, cor=cor_hexadecimal))

            if forma != None:
                self.elementosGeometricos.append(forma)
                self.lista_elementos.insert(tk.END, forma.nome)
                self.salvar_formas_em_obj()
                self.redraw()

        except Exception as erro:
            print("ERRO!")
            
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