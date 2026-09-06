import tkinter as tk
from formas_geometricas import FormasGeometricas
from transfromadas_objetos import TransformarObjetos

# ================================
# CLASSE JANELA DE TRANSFORMAÇÕES
# ================================

class JanelaTransformacoes:

    def __init__(self, janela_pai, elemento, aplicacao_principal):
        self.elemento = elemento
        self.aplicacao_principal = (aplicacao_principal)
        self.transformacoes = []
        self.janela = tk.Toplevel(janela_pai)
        self.janela.title(f"TRANSFORMAR: {self.elemento.nome}")
        self.janela.geometry("650x450")
        self.janela.wait_visibility()
        self.janela.grab_set()
        self.criar_interface()


    # =================================
    # INTERFACE EM SI (BOTÕES E LISTA)
    # =================================

    def criar_interface(self):
        frame_principal = tk.Frame(self.janela, padx=10, pady=10)
        frame_principal.pack(fill="both", expand=True)

        frame_esquerda = tk.Frame(frame_principal)
        frame_esquerda.pack(side="left", fill="y", padx=(0, 20))

    # ====================================
    # botões e cédula para inserir valores

        tk.Label(frame_esquerda, text="Translação (xp, yp):", font=("Times New Roman", 10, "bold")).pack(pady=(0, 5))
        regiao_translacao = tk.Frame(frame_esquerda)
        regiao_translacao.pack(pady=(0, 15))
        self.recebido_translacao_dx = tk.Entry(regiao_translacao, width=5)
        self.recebido_translacao_dx.pack(side="left", padx=2)
        self.recebido_translacao_dy = tk.Entry(regiao_translacao, width=5)
        self.recebido_translacao_dy.pack(side="left", padx=2)
        tk.Button(regiao_translacao, text="Adicionar", font=("Times New Roman", 10, "bold"), command=self.adicionar_translacao).pack(side="left", padx=5)

        tk.Label(frame_esquerda, text="Rotação em torno do centro do objeto (Graus):", font=("Times New Roman", 10, "bold")).pack(pady=(5, 5))
        regiao_rotacao = tk.Frame(frame_esquerda)
        regiao_rotacao.pack(pady=(0, 15))
        self.recebido_angulo_rotacao_c_o = tk.Entry(regiao_rotacao, width=10)
        self.recebido_angulo_rotacao_c_o.pack(side="left", padx=2)
        tk.Button(regiao_rotacao, text="Adicionar", font=("Times New Roman", 10, "bold"), command=self.adicionar_rotacao_centro_objeto).pack(side="left", padx=5)

        tk.Label(frame_esquerda, text="Rotação em torno do centro do mundo (Graus):", font=("Times New Roman", 10, "bold")).pack(pady=(5, 5))
        regiao_rotacao_origem = tk.Frame(frame_esquerda)
        regiao_rotacao_origem.pack(pady=(0, 15))
        self.recebido_angulo_rotacao_c_m = tk.Entry(regiao_rotacao_origem, width=10)
        self.recebido_angulo_rotacao_c_m.pack(side="left", padx=2)
        tk.Button(regiao_rotacao_origem, text="Adicionar", font=("Times New Roman", 10, "bold"), command=self.adicionar_rotacao_centro_mundo).pack(side="left", padx=5)

        tk.Label(frame_esquerda, text="Rotação em torno de um ponto qualquer (Graus, X, Y):", font=("Times New Roman", 10, "bold")).pack(pady=(5, 5))
        regiao_rotacao_arbitrario = tk.Frame(frame_esquerda)
        regiao_rotacao_arbitrario.pack(pady=(0, 15))
        self.recebido_angulo_rotacao_p_a = tk.Entry(regiao_rotacao_arbitrario, width=5)
        self.recebido_angulo_rotacao_p_a.pack(side="left", padx=2)
        self.recebido_rotacao_pa_x = tk.Entry(regiao_rotacao_arbitrario, width=5)
        self.recebido_rotacao_pa_x.pack(side="left", padx=2)
        self.recebido_rotacao_pa_y = tk.Entry(regiao_rotacao_arbitrario, width=5)
        self.recebido_rotacao_pa_y.pack(side="left", padx=2)
        tk.Button(regiao_rotacao_arbitrario, text="Adicionar", font=("Times New Roman", 10, "bold"), command=self.adicionar_rotacao_ponto_arbitrario).pack(side="left", padx=5)

        tk.Label(frame_esquerda, text="Escalonamento (Sx, Sy):", font=("Times New Roman", 10, "bold")).pack(pady=(5, 5))
        regiao_escalonamento = tk.Frame(frame_esquerda)
        regiao_escalonamento.pack(pady=(0, 15))
        self.recebido_escalonamento_sx = tk.Entry(regiao_escalonamento, width=5)
        self.recebido_escalonamento_sx.pack(side="left", padx=2)
        self.recebido_escalonamento_sy = tk.Entry(regiao_escalonamento, width=5)
        self.recebido_escalonamento_sy.pack(side="left", padx=2)
        tk.Button(regiao_escalonamento, text="Adicionar", font=("Times New Roman", 10, "bold"), command=self.adicionar_escalonamento).pack(side="left", padx=5)

    # =============================
    # fazer lista das transformadas

        frame_direita = tk.Frame(frame_principal)
        frame_direita.pack(side="right", fill="both", expand=True)
        tk.Label(frame_direita, text="Fila de Transformações:", font=("Times New Roman", 12, "bold")).pack(anchor="w", pady=(0, 5))
        frame_lista = tk.Frame(frame_direita)
        frame_lista.pack(fill="both", expand=True, pady=(0, 10))
        self.lista_transformacoes = tk.Listbox(frame_lista, bg="white", height=12)
        self.lista_transformacoes.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(frame_lista, orient="vertical", command=self.lista_transformacoes.yview)
        scrollbar.pack(side="right", fill="y")

        self.lista_transformacoes.config(yscrollcommand=scrollbar.set)

    # ========================================
    # botão que envia todas as transformações

        tk.Button(frame_direita, text="Aplicar transformações", font=("Times New Roman", 11, "bold"), command=self.realizar_transformacoes_forma).pack(fill="x")

    # ========================================
    # O QUE OCORRE QUANDO SE APERTA UM BOTÃO?
    # ========================================

    def adicionar_translacao(self):
        translacao_dx = float(self.recebido_translacao_dx.get())
        translacao_dy = float(self.recebido_translacao_dy.get())
        self.transformacoes.append(["translacao", translacao_dx, translacao_dy])
        self.lista_transformacoes.insert(tk.END, "Translação: X={}, Y={}".format(translacao_dx, translacao_dy))
        self.recebido_translacao_dx.delete(0,tk.END)
        self.recebido_translacao_dy.delete(0,tk.END)

    def adicionar_rotacao_centro_objeto(self):
        angulo = float(self.recebido_angulo_rotacao_c_o.get())
        self.transformacoes.append(["rotacao_centro_objeto", angulo])
        self.lista_transformacoes.insert(tk.END,"Rotação centro objeto: {}°".format(angulo))
        self.recebido_angulo_rotacao_c_o.delete(0,tk.END)

    def adicionar_rotacao_centro_mundo(self):
        angulo = float(self.recebido_angulo_rotacao_c_m.get())
        self.transformacoes.append(["rotacao_centro_mundo", angulo])
        self.lista_transformacoes.insert(tk.END,"Rotação centro mundo: {}°".format(angulo))
        self.recebido_angulo_rotacao_c_m.delete(0,tk.END)

    def adicionar_rotacao_ponto_arbitrario(self):
        angulo = float(self.recebido_angulo_rotacao_p_a.get())
        x = float(self.recebido_rotacao_pa_x.get())
        y = float(self.recebido_rotacao_pa_y.get())
        self.transformacoes.append(["rotacao_ponto_arbitrario", angulo, x, y])
        self.lista_transformacoes.insert(tk.END, "Rotação ponto arbitrário: {}°, X={}, Y={}".format(angulo, x, y))
        self.recebido_angulo_rotacao_p_a.delete(0,tk.END)
        self.recebido_rotacao_pa_x.delete(0,tk.END)
        self.recebido_rotacao_pa_y.delete(0,tk.END)

    def adicionar_escalonamento(self):
        sx = float(self.recebido_escalonamento_sx.get())
        sy = float(self.recebido_escalonamento_sy.get())
        self.transformacoes.append(["escalonamento", sx, sy])
        self.lista_transformacoes.insert(tk.END, "Escalonamento: Sx={}, Sy={}".format(sx,sy))
        self.recebido_escalonamento_sx.delete(0, tk.END)
        self.recebido_escalonamento_sy.delete(0, tk.END)

    # =======================================================================================
    # pega todas as transformações faz a matriz e depois de pegar todas as matrizes, calcula

    def realizar_transformacoes_forma(self):
        transformador = TransformarObjetos()
        matriz_acomulada = None
        x_centro, y_centro = transformador.centro_poligono(self.elemento.pontos)        
        for i in range(len(self.transformacoes)):
            tipo_transf = self.transformacoes[i][0]
            if tipo_transf == "translacao":
                matriz_transformada = transformador.fazer_matriz_translacao(self.transformacoes[i][1], self.transformacoes[i][2])
            elif tipo_transf == "rotacao_centro_objeto":
                if matriz_acomulada is None:
                    x_centro_atual = x_centro
                    y_centro_atual = y_centro
                else:
                    ponto_centro = [[x_centro, y_centro, 1]]
                    novo_centro = transformador.multiplicacao_matrizes(ponto_centro, matriz_acomulada)
                    x_centro_atual = novo_centro[0][0]
                    y_centro_atual = novo_centro[0][1]
                matriz_transformada = transformador.fazer_matriz_rotacao_centro_objeto(self.transformacoes[i][1], x_centro_atual, y_centro_atual)
            elif tipo_transf == "escalonamento":
                if matriz_acomulada is None:
                    x_centro_atual = x_centro
                    y_centro_atual = y_centro
                else:
                    ponto_centro = [[x_centro, y_centro, 1]]
                    novo_centro = transformador.multiplicacao_matrizes(ponto_centro, matriz_acomulada)
                    x_centro_atual = novo_centro[0][0]
                    y_centro_atual = novo_centro[0][1]
                matriz_transformada = transformador.fazer_matriz_escalonamento(self.transformacoes[i][1], self.transformacoes[i][2], x_centro_atual, y_centro_atual)
                
            elif tipo_transf == "rotacao_ponto_arbitrario":
                matriz_transformada = transformador.fazer_matriz_rotacao_ponto_arbritario(self.transformacoes[i][1], self.transformacoes[i][2], self.transformacoes[i][3])
                
            elif tipo_transf == "rotacao_centro_mundo":
                matriz_transformada = transformador.fazer_matriz_rotacao_centro_mundo(self.transformacoes[i][1])
                
            else:
                print("ERRO!")
            if matriz_acomulada is None:
                matriz_acomulada = matriz_transformada
            else:
                matriz_acomulada = transformador.multiplicacao_matrizes(matriz_acomulada, matriz_transformada)
        if matriz_acomulada is not None:
            novos_pontos = transformador.aplicar_matriz_transformacao(self.elemento.pontos, matriz_acomulada)
            self.elemento.pontos = novos_pontos

        self.aplicacao_principal.redraw()
        self.aplicacao_principal.salvar_formas_em_obj()
        self.janela.destroy()
