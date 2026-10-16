import random
import tkinter as tk
from viewport import ViewPoint
import math

cores = ["#ff0000", "#bb00ff", "#008000", "#ffff00", "#ffa500", "#800080", "#000000"]

# ==============================
# CLASSE FORMAS GEOMÉTRICAS
# ==============================

class FormasGeometricas:
    def __init__(self, nome: str, tipo: str, pontos: list, conexoes: list = None, cor: str = None):
        self.nome = nome   
        self.tipo = tipo   
        self.pontos = pontos
        
        self.conexoes = conexoes
        if not self.conexoes:
            if self.tipo == "ponto": self.conexoes = [[0]]
            elif self.tipo == "linha": self.conexoes = [[0, 1]]
            else: self.conexoes = [list(range(len(self.pontos)))]
            
        self.cor = cor if cor else random.choice(cores)

    # ==============================
    # É desenhado na tela as figuras

    def adiconar_na_tela(self, canvas: tk.Canvas, vp: ViewPoint):
        if self.tipo == "CAMERA": return 

        for conexao in self.conexoes:
            pontos_3d_face = []
            for idx in conexao:
                if idx < len(self.pontos):
                    pontos_3d_face.append(self.pontos[idx])
            
            if not pontos_3d_face: continue

            if self.tipo == "wireframe" or self.tipo == "linha":
                tamanho = len(pontos_3d_face)
                for j in range(tamanho):
                    if self.tipo == "linha" and j == tamanho - 1: break
                    p1 = pontos_3d_face[j]
                    p2 = pontos_3d_face[(j + 1) % tamanho]
                    
                    pts_tela = vp.RealizarNormalizacao([p1, p2], "linha")
                    if pts_tela and len(pts_tela) == 2 and pts_tela[0] and pts_tela[1]:
                        x1, y1 = pts_tela[0]; x2, y2 = pts_tela[1]
                        canvas.create_line(x1, y1, x2, y2, fill=self.cor)
                    
            elif self.tipo == "poligono_preenchido":
                pts_tela = vp.RealizarNormalizacao(pontos_3d_face, "poligono_preenchido")
                if pts_tela and len(pts_tela) >= 3 and all(pts_tela):
                    canvas.create_polygon(pts_tela, fill=self.cor, outline=self.cor, width=1)
                    
            elif self.tipo == "ponto":
                pts_tela = vp.RealizarNormalizacao(pontos_3d_face, "ponto")
                if pts_tela and pts_tela[0]:
                    x, y = pts_tela[0]
                    canvas.create_line(x, y, x+1, y, fill=self.cor)

# ==============================
# CLASSE OBJETO WINDOW
# ==============================

class ObjetoWindow(FormasGeometricas):
    def __init__(self, vp):
        self.vp = vp
        self.nome = "WINDOW_CAMERA"
        self.tipo = "CAMERA"
        self.cor = "#000000"
        self.pontos = [(vp.vrp[0], vp.vrp[1], vp.vrp[2])]

    def adiconar_na_tela(self, canvas, vp):
        pass 

    def aplicar_transformacao_3d(self, matriz_4x4, transformador):
        p_vrp = [[self.vp.vrp[0], self.vp.vrp[1], self.vp.vrp[2], 1]]
        p_vpn = [[self.vp.vrp[0]+self.vp.vpn[0], self.vp.vrp[1]+self.vp.vpn[1], self.vp.vrp[2]+self.vp.vpn[2], 1]]
        p_vup = [[self.vp.vrp[0]+self.vp.vup[0], self.vp.vrp[1]+self.vp.vup[1], self.vp.vrp[2]+self.vp.vup[2], 1]]
        
        n_vrp = transformador.multiplicacao_matrizes(p_vrp, matriz_4x4)[0]
        n_vpn = transformador.multiplicacao_matrizes(p_vpn, matriz_4x4)[0]
        n_vup = transformador.multiplicacao_matrizes(p_vup, matriz_4x4)[0]
        
        self.vp.vrp = [n_vrp[0], n_vrp[1], n_vrp[2]]
        
        vetor_vpn_novo = [n_vpn[0]-n_vrp[0], n_vpn[1]-n_vrp[1], n_vpn[2]-n_vrp[2]]
        mod_vpn = math.sqrt(vetor_vpn_novo[0]**2 + vetor_vpn_novo[1]**2 + vetor_vpn_novo[2]**2)
        self.vp.vpn = [0, 0, 0] if mod_vpn == 0 else [vetor_vpn_novo[0]/mod_vpn, vetor_vpn_novo[1]/mod_vpn, vetor_vpn_novo[2]/mod_vpn]
        
        vetor_vup_novo = [n_vup[0]-n_vrp[0], n_vup[1]-n_vrp[1], n_vup[2]-n_vrp[2]]
        mod_vup = math.sqrt(vetor_vup_novo[0]**2 + vetor_vup_novo[1]**2 + vetor_vup_novo[2]**2)
        self.vp.vup = [0, 0, 0] if mod_vup == 0 else [vetor_vup_novo[0]/mod_vup, vetor_vup_novo[1]/mod_vup, vetor_vup_novo[2]/mod_vup]
        
        self.pontos = [(self.vp.vrp[0], self.vp.vrp[1], self.vp.vrp[2])]