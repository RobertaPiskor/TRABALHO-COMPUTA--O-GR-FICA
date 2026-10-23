import tkinter as tk
from tkinter import messagebox
from transfromadas_objetos import TransformarObjetos

# ================================
# CLASSE JANELA DE TRANSFORMAÇÕES
# ================================

class JanelaTransformacoes:
    def __init__(self, janela_pai, elemento, aplicacao_principal):
        self.elemento = elemento
        self.aplicacao_principal = aplicacao_principal
        self.transformacoes = []
        self.janela = tk.Toplevel(janela_pai)
        self.janela.title(f"TRANSFORMAR: {self.elemento.nome}")
        self.janela.geometry("700x550")
        self.janela.grab_set()
        self.criar_interface()

    # =================================
    # INTERFACE EM SI (BOTÕES E LISTA)
    # =================================

    def criar_interface(self):
        f_esq = tk.Frame(self.janela, padx=10, pady=10)
        f_esq.pack(side="left", fill="y")
        f_dir = tk.Frame(self.janela, padx=10, pady=10)
        f_dir.pack(side="right", fill="both", expand=True)

    # ====================================
    # botões e cédula para inserir valores

        tk.Label(f_esq, text="Translação (DX, DY, DZ):", font=("Times New Roman", 10, "bold")).pack(pady=(5,2))
        f_trans = tk.Frame(f_esq); f_trans.pack()
        self.ent_dx = tk.Entry(f_trans, width=5); self.ent_dx.pack(side="left", padx=2)
        self.ent_dy = tk.Entry(f_trans, width=5); self.ent_dy.pack(side="left", padx=2)
        self.ent_dz = tk.Entry(f_trans, width=5); self.ent_dz.pack(side="left", padx=2)
        tk.Button(f_trans, text="Adicionar", command=lambda: self.adicionar_transformacao("translacao")).pack(side="left", padx=2)

        tk.Label(f_esq, text="Escalonamento (SX, SY, SZ):", font=("Times New Roman", 10, "bold")).pack(pady=(15,2))
        f_esc = tk.Frame(f_esq); f_esc.pack()
        self.ent_sx = tk.Entry(f_esc, width=5); self.ent_sx.pack(side="left", padx=2)
        self.ent_sy = tk.Entry(f_esc, width=5); self.ent_sy.pack(side="left", padx=2)
        self.ent_sz = tk.Entry(f_esc, width=5); self.ent_sz.pack(side="left", padx=2)
        tk.Button(f_esc, text="Adicionar", command=lambda: self.adicionar_transformacao("escalonamento")).pack(side="left", padx=2)

        tk.Label(f_esq, text="Rotação no Centro do Objeto:", font=("Times New Roman", 10, "bold")).pack(pady=(15,2))
        f_rot = tk.Frame(f_esq); f_rot.pack()
        tk.Label(f_rot, text="Ângulo:").pack(side="left")
        self.ent_ang_c = tk.Entry(f_rot, width=5); self.ent_ang_c.pack(side="left", padx=2)
        self.var_eixo = tk.StringVar(value="X")
        tk.OptionMenu(f_rot, self.var_eixo, "X", "Y", "Z").pack(side="left", padx=2)
        tk.Button(f_rot, text="Adicionar", command=lambda: self.adicionar_transformacao("rot_centro")).pack(side="left", padx=2)

        tk.Label(f_esq, text="Rotação no Centro do Mundo (0,0,0):", font=("Times New Roman", 10, "bold")).pack(pady=(15,2))
        f_rot_m = tk.Frame(f_esq); f_rot_m.pack()
        tk.Label(f_rot_m, text="Ângulo:").pack(side="left")
        self.ent_ang_m = tk.Entry(f_rot_m, width=5); self.ent_ang_m.pack(side="left", padx=2)
        self.var_eixo_m = tk.StringVar(value="X")
        tk.OptionMenu(f_rot_m, self.var_eixo_m, "X", "Y", "Z").pack(side="left", padx=2)
        tk.Button(f_rot_m, text="Adicionar", command=lambda: self.adicionar_transformacao("rot_mundo")).pack(side="left", padx=2)

        tk.Label(f_esq, text="Rotação Eixo Arbitrário (Ang, P1x,y,z, P2x,y,z):", font=("Times New Roman", 10, "bold")).pack(pady=(15,2))
        f_arb = tk.Frame(f_esq); f_arb.pack()
        self.ent_ang_arb = tk.Entry(f_arb, width=4); self.ent_ang_arb.pack(side="left")
        self.ent_p1x = tk.Entry(f_arb, width=3); self.ent_p1x.pack(side="left")
        self.ent_p1y = tk.Entry(f_arb, width=3); self.ent_p1y.pack(side="left")
        self.ent_p1z = tk.Entry(f_arb, width=3); self.ent_p1z.pack(side="left")
        self.ent_p2x = tk.Entry(f_arb, width=3); self.ent_p2x.pack(side="left")
        self.ent_p2y = tk.Entry(f_arb, width=3); self.ent_p2y.pack(side="left")
        self.ent_p2z = tk.Entry(f_arb, width=3); self.ent_p2z.pack(side="left")
        tk.Button(f_arb, text="Adicionar", command=lambda: self.adicionar_transformacao("rot_arb")).pack(side="left")

        # =============================
        # fazer lista das transformadas
        tk.Label(f_dir, text="Fila de Transformações:", font=("Times New Roman", 12, "bold")).pack(anchor="w")
        self.lista = tk.Listbox(f_dir, bg="white", height=15); self.lista.pack(fill="both", expand=True, pady=(0,10))
        tk.Button(f_dir, text="Aplicar Transformações", font=("Times New Roman", 11, "bold"), command=self.realizar_transformacoes_forma).pack(fill="x")

    def adicionar_transformacao(self, tipo):
        try:
            if tipo == "translacao":
                dx = float(self.ent_dx.get() or 0.0)
                dy = float(self.ent_dy.get() or 0.0)
                dz = float(self.ent_dz.get() or 0.0)
                self.transformacoes.append(["translacao", dx, dy, dz])
                self.lista.insert(tk.END, f"Translação: X={dx}, Y={dy}, Z={dz}")
                self.ent_dx.delete(0, tk.END); self.ent_dy.delete(0, tk.END); self.ent_dz.delete(0, tk.END)
                
            elif tipo == "escalonamento":
                sx = float(self.ent_sx.get() or 1.0)
                sy = float(self.ent_sy.get() or 1.0)
                sz = float(self.ent_sz.get() or 1.0)
                self.transformacoes.append(["escalonamento", sx, sy, sz])
                self.lista.insert(tk.END, f"Escalonamento: Sx={sx}, Sy={sy}, Sz={sz}")
                self.ent_sx.delete(0, tk.END); self.ent_sy.delete(0, tk.END); self.ent_sz.delete(0, tk.END)
                
            elif tipo == "rot_centro":
                ang = float(self.ent_ang_c.get() or 0.0)
                eixo = self.var_eixo.get()
                self.transformacoes.append(["rot_centro", ang, eixo])
                self.lista.insert(tk.END, f"Rotação Centro {eixo}: {ang}°")
                self.ent_ang_c.delete(0, tk.END)

            elif tipo == "rot_mundo":
                ang = float(self.ent_ang_m.get() or 0.0)
                eixo = self.var_eixo_m.get()
                self.transformacoes.append(["rot_mundo", ang, eixo])
                self.lista.insert(tk.END, f"Rotação Mundo {eixo}: {ang}°")
                self.ent_ang_m.delete(0, tk.END)
                
            elif tipo == "rot_arb":
                ang = float(self.ent_ang_arb.get() or 0.0)
                p1 = [float(self.ent_p1x.get() or 0.0), float(self.ent_p1y.get() or 0.0), float(self.ent_p1z.get() or 0.0)]
                p2 = [float(self.ent_p2x.get() or 0.0), float(self.ent_p2y.get() or 0.0), float(self.ent_p2z.get() or 0.0)]
                self.transformacoes.append(["rot_arb", ang, p1, p2])
                self.lista.insert(tk.END, f"Rotação Eixo Arbitrário: {ang}°")
                self.ent_ang_arb.delete(0, tk.END)
                self.ent_p1x.delete(0, tk.END); self.ent_p1y.delete(0, tk.END); self.ent_p1z.delete(0, tk.END)
                self.ent_p2x.delete(0, tk.END); self.ent_p2y.delete(0, tk.END); self.ent_p2z.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Erro", "Por favor, digite valores numéricos válidos!")

    def realizar_transformacoes_forma(self):
        transformacao = TransformarObjetos()
        matriz_acumulada = transformacao.matriz_identidade()
        
        if getattr(self.elemento, 'tipo', '') == "CAMERA": 
            cx, cy, cz = self.elemento.vp.vrp
        else: 
            cx, cy, cz = transformacao.centro_poligono(self.elemento.pontos)
        
        for op in self.transformacoes:
            tipo = op[0]
            if tipo == "translacao": 
                m = transformacao.fazer_matriz_translacao(op[1], op[2], op[3])
            elif tipo == "escalonamento": 
                m = transformacao.fazer_matriz_escalonamento(op[1], op[2], op[3], cx, cy, cz)
            elif tipo == "rot_centro":
                if op[2] == "X": r = transformacao.fazer_matriz_rotacao_x(op[1])
                elif op[2] == "Y": r = transformacao.fazer_matriz_rotacao_y(op[1])
                else: r = transformacao.fazer_matriz_rotacao_z(op[1])
                ida = transformacao.fazer_matriz_translacao(-cx, -cy, -cz)
                volta = transformacao.fazer_matriz_translacao(cx, cy, cz)
                m = transformacao.multiplicacao_matrizes(transformacao.multiplicacao_matrizes(ida, r), volta)
            elif tipo == "rot_mundo":
                if op[2] == "X": m = transformacao.fazer_matriz_rotacao_x(op[1])
                elif op[2] == "Y": m = transformacao.fazer_matriz_rotacao_y(op[1])
                else: m = transformacao.fazer_matriz_rotacao_z(op[1])
            elif tipo == "rot_arb": 
                m = transformacao.fazer_matriz_rotacao_eixo_arbitrario(op[1], op[2], op[3])
            
            nc = transformacao.multiplicacao_matrizes([[cx, cy, cz, 1]], m)[0]
            cx, cy, cz = nc[0], nc[1], nc[2]

        matriz_acumulada = transformacao.multiplicacao_matrizes(matriz_acumulada, m)

        if getattr(self.elemento, 'tipo', '') == "CAMERA": 
            self.elemento.aplicar_transformacao_3d(matriz_acumulada, transformacao)
        elif getattr(self.elemento, 'tipo', '') == "curva":
            # Aplica transformação aos pontos de controle primeiro
            self.elemento.pontos_controle = transformacao.aplicar_matriz_transformacao(self.elemento.pontos_controle, matriz_acumulada)
            # Recalcula a curva com os novos pontos
            if self.elemento.tipo_curva == "bspline":
                self.elemento.pontos = self.elemento.calcular_b_splines_com_Forward_differences(self.elemento.pontos_controle)
            else:
                self.elemento.pontos = self.elemento.calcular_curva_bezier(self.elemento.pontos_controle)
        else: 
            self.elemento.pontos = transformacao.aplicar_matriz_transformacao(self.elemento.pontos, matriz_acumulada)

        self.aplicacao_principal.redraw()
        
        if getattr(self.elemento, 'tipo', '') not in ["curva", "CAMERA"]:
            self.aplicacao_principal.salvar_formas_em_obj()
            
        self.janela.destroy()