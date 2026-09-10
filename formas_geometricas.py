import math
import random
import tkinter as tk
from viewport import ViewPoint

cores = ["#ff0000", "#bb00ff", "#008000", "#ffff00", "#ffa500", "#800080", "#ffc0cb", "#a52a2a", "#000000", "#ffffff", "#808080", "#00ffff", "#ff00ff", "#00ff00", "#000080", "#008080", "#808000", "#800000", "#00ffff", "#ffd700", "#c0c0c0", "#ff7f50", "#ff6347", "#fa8072", "#ee82ee", "#4b0082", "#40e0d0", "#f5f5dc", "#dc143c", "#f0e68c"]

# ==============================
# CLASSE FORMAS GEOMÉTRICAS
# ==============================

class FormasGeometricas:
    def __init__(self, nome: str, tipo: str, pontos: list, cor: str):
        self.nome = nome   
        self.tipo = tipo   
        self.pontos = pontos
        self.cor = cor

    # ==============================
    # É desenhado na tela as figuras

    def adiconar_na_tela(self, canvas: tk.Canvas, vp: ViewPoint):
        pontos_tela = vp.RealizarNormalizacao(self.pontos)
        if self.tipo == "ponto":
            xvp, yvp = pontos_tela[0]
            canvas.create_line(xvp, yvp, xvp+1, yvp, fill=self.cor)
        elif self.tipo == "linha":
            x1vp, y1vp = pontos_tela[0]
            x2vp, y2vp = pontos_tela[1]
            canvas.create_line(x1vp, y1vp, x2vp, y2vp, fill=self.cor)
        else:
            for j in range(len(pontos_tela) - 1):
                xvp1, yvp1 = pontos_tela[j]
                xvp2, yvp2 = pontos_tela[j+1]
                canvas.create_line(xvp1, yvp1, xvp2, yvp2, fill=self.cor)    
            xvp1, yvp1 = pontos_tela[-1]
            xvp2, yvp2 = pontos_tela[0]
            canvas.create_line(xvp1, yvp1, xvp2, yvp2, fill=self.cor)
            
    # ==============================
    # CRIAÇÃO DAS FIGURAS
    # ==============================

    @classmethod
    def drawPixel(cls, c: tk.Canvas, x: float, y: float, cor: str = None):
        if cor is None:
            cor = random.choice(cores)
        c.create_line(x, y, x, y+1, fill=cor)

    @classmethod
    def drawPoint(cls, nome: str, cx: float, cy: float, cor: str = None):
        if cor is None:
            cor = random.choice(cores)
        pontos = [(cx, cy)]
        return cls(nome, "ponto", pontos, cor)

    @classmethod
    def drawCircle(cls, nome: str, cx: float, cy: float, raio: float, cor: str = None):
        if cor is None:
            cor = random.choice(cores)
        pontos = []
        for i in range(360):
            x = cx + raio * math.cos(2 * math.pi * i / 360)
            y = cy + raio * math.sin(2 * math.pi * i / 360)
            pontos.append((x, y))
        return cls(nome, "circulo", pontos, cor)

    @classmethod
    def drawLine(cls, nome: str, x1: float, y1: float, x2: float, y2: float, cor: str = None):
        if cor is None:
            cor = random.choice(cores)
        pontos = [(x1, y1), (x2, y2)]
        return cls(nome, "linha", pontos, cor)

    @classmethod
    def drawSquere(cls, nome: str, xi: float, yi: float, tamanho: float, cor: str = None):
        if cor is None:
            cor = random.choice(cores)
        pontos = [(xi, yi), (xi + tamanho, yi), (xi + tamanho, yi + tamanho), (xi, yi + tamanho)]    
        return cls(nome, "quadrado", pontos, cor)

    @classmethod
    def drawWireframe(cls, nome: str, pontos: list, cor: str = None):
        if cor is None:
            cor = random.choice(cores)
        return cls(nome, "wireframe", pontos, cor)