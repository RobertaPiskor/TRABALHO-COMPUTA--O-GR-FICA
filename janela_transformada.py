import tkinter as tk

from formas_geometricas import FormasGeometricas


class JanelaTransformacoes:

    def __init__(self, master, elemento, callback_atualizar):
        self.elemento = elemento
        self.callback_atualizar = (callback_atualizar)
        self.transformacoes = []
        self.janela = tk.Toplevel(master)
        self.janela.title(f"Transformar: {self.elemento.nome}")
        self.janela.geometry("650x450")
        self.janela.grab_set()
        self.criar_interface()


    # ==========================================================
    # INTERFACE
    # ==========================================================

    def criar_interface(self):
        frame_principal = tk.Frame(self.janela, padx=10, pady=10)
        frame_principal.pack(fill="both", expand=True)

        frame_esquerda = tk.Frame(frame_principal)
        frame_esquerda.pack(side="left", fill="y", padx=(0, 20))

        tk.Label(frame_esquerda, text="Translação (xp, yp):", font=("Times New Roman", 10, "bold")).pack(pady=(0, 5))
        frame_trans = tk.Frame(frame_esquerda)
        frame_trans.pack(pady=(0, 15))
        self.recebido_translacao_dx = tk.Entry(frame_trans, width=5)
        self.recebido_translacao_dx.pack(side="left", padx=2)
        self.recebido_translacao_dy = tk.Entry(frame_trans, width=5)
        self.recebido_translacao_dy.pack(side="left", padx=2)
        tk.Button(frame_trans, text="Adicionar", font=("Times New Roman", 10, "bold"), command=self.adicionar_translacao).pack(side="left", padx=5)

        tk.Label(frame_esquerda, text="Rotação em torno do centro do objeto (Graus):", font=("Times New Roman", 10, "bold")).pack(pady=(5, 5))
        frame_rot = tk.Frame(frame_esquerda)
        frame_rot.pack(pady=(0, 15))
        self.recebido_angulo_rotacao_c_o = tk.Entry(frame_rot, width=10)
        self.recebido_angulo_rotacao_c_o.pack(side="left", padx=2)
        tk.Button(frame_rot, text="Adicionar", font=("Times New Roman", 10, "bold"), command=self.adicionar_rotacao_centro_objeto).pack(side="left", padx=5)

        tk.Label(frame_esquerda, text="Rotação em torno do centro do mundo (Graus):", font=("Times New Roman", 10, "bold")).pack(pady=(5, 5))
        frame_rot_orig = tk.Frame(frame_esquerda)
        frame_rot_orig.pack(pady=(0, 15))
        self.recebido_angulo_rotacao_c_m = tk.Entry(frame_rot_orig, width=10)
        self.recebido_angulo_rotacao_c_m.pack(side="left", padx=2)
        tk.Button(frame_rot_orig, text="Adicionar", font=("Times New Roman", 10, "bold"), command=self.adicionar_rotacao_centro_mundo).pack(side="left", padx=5)

        tk.Label(frame_esquerda, text="Rotação em torno de um ponto qualquer (Graus, X, Y):", font=("Times New Roman", 10, "bold")).pack(pady=(5, 5))
        frame_rot_arb = tk.Frame(frame_esquerda)
        frame_rot_arb.pack(pady=(0, 15))
        self.recebido_angulo_rotacao_p_a = tk.Entry(frame_rot_arb, width=5)
        self.recebido_angulo_rotacao_p_a.pack(side="left", padx=2)
        self.recebido_rotacao_pa_x = tk.Entry(frame_rot_arb, width=5)
        self.recebido_rotacao_pa_x.pack(side="left", padx=2)
        self.recebido_rotacao_pa_y = tk.Entry(frame_rot_arb, width=5)
        self.recebido_rotacao_pa_y.pack(side="left", padx=2)
        tk.Button(frame_rot_arb, text="Adicionar", font=("Times New Roman", 10, "bold"), command=self.adicionar_rotacao_ponto_arbitrario).pack(side="left", padx=5)

        tk.Label(frame_esquerda, text="Escalonamento (Sx, Sy):", font=("Times New Roman", 10, "bold")).pack(pady=(5, 5))
        frame_esc = tk.Frame(frame_esquerda)
        frame_esc.pack(pady=(0, 15))
        self.recebido_escalonamento_sx = tk.Entry(frame_esc, width=5)
        self.recebido_escalonamento_sx.pack(side="left", padx=2)
        self.recebido_escalonamento_sy = tk.Entry(frame_esc, width=5)
        self.recebido_escalonamento_sy.pack(side="left", padx=2)
        tk.Button(frame_esc, text="Adicionar", font=("Times New Roman", 10, "bold"), command=self.adicionar_escalonamento).pack(side="left", padx=5)

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

        tk.Button(frame_direita, text="Aplicar transformações", font=("Times New Roman", 11, "bold"), command=self.realizar_transformacoes_forma).pack(fill="x")

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
        self.lista_transformacoes.insert(tk.END, "Rotação ponto arbitrário: {}°".format(angulo))
        self.recebido_angulo_rotacao_p_a.delete(0,tk.END)
        self.recebido_rotacao_pa_x.delete(0,tk.END)
        self.recebido_rotacao_pa_y.delete(0,tk.END)

    def adicionar_escalonamento(self):
        sx = float(self.recebido_escalonamento_sx.get())
        sy = float(self.recebido_escalonamento_sy.get())
        self.transformacoes.append(["escalonamento", sx, sy])
        self.lista_transformacoes.insert(tk.END, f"Escalonamento: Sx={sx}, Sy={sy}")
        self.recebido_escalonamento_sx.delete(0, tk.END)
        self.recebido_escalonamento_sy.delete(0, tk.END)

    def realizar_transformacoes_forma(self):
        matriz_acomulada = None
        for i in range(len(self.transformacoes)):
            if (self.transformacoes[i][0] == "translacao"):
                matriz_transformada = self.elemento.fazer_matriz_translacao(self.transformacoes[i][1], self.transformacoes[i][2])
                if (matriz_acomulada != None):
                    matriz_resultado = FormasGeometricas.multiplicacao_matrizes(matriz_acomulada, matriz_transformada)
                    matriz_acomulada = matriz_resultado
                else:
                    matriz_acomulada = matriz_transformada
            elif (self.transformacoes[i][0] == "rotacao_centro_objeto"):
                if (matriz_acomulada != None):
                    self.elemento.aplicar_matriz_transformacao(matriz_acomulada)
                    matriz_acomulada = None
                matriz_transformada = self.elemento.fazer_matriz_rotacao_centro_objeto(self.transformacoes[i][1])
                matriz_acomulada = matriz_transformada
            elif (self.transformacoes[i][0] == "escalonamento"):
                if (matriz_acomulada != None):
                    self.elemento.aplicar_matriz_transformacao(matriz_acomulada)
                    matriz_acomulada = None
                matriz_transformada = self.elemento.fazer_matriz_escalonamento(self.transformacoes[i][1], self.transformacoes[i][2])
                matriz_acomulada = matriz_transformada
            elif (self.transformacoes[i][0] == "rotacao_ponto_arbitrario"):
                matriz_transformada = self.elemento.fazer_matriz_rotacao_ponto_arbritario(self.transformacoes[i][1], self.transformacoes[i][2], self.transformacoes[i][3])
                if (matriz_acomulada != None):
                    matriz_resultado = FormasGeometricas.multiplicacao_matrizes(matriz_acomulada, matriz_transformada)
                    matriz_acomulada = matriz_resultado
                else:
                    matriz_acomulada = matriz_transformada
            elif (self.transformacoes[i][0] == "rotacao_centro_mundo"):
                matriz_transformada = self.elemento.fazer_matriz_rotacao_centro_mundo(self.transformacoes[i][1])
                if (matriz_acomulada != None):
                    matriz_resultado = FormasGeometricas.multiplicacao_matrizes(matriz_acomulada, matriz_transformada)
                    matriz_acomulada = matriz_resultado
                else:
                    matriz_acomulada = matriz_transformada
            else:
                print("ERRO!")
        if (matriz_acomulada != None):
            self.elemento.aplicar_matriz_transformacao(matriz_acomulada)

        self.callback_atualizar()
        self.janela.destroy()