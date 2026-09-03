import math
import random
import tkinter as tk
from viewport import ViewPoint

cores = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "black", "white", "gray", "cyan", "magenta", "lime", "navy", "teal", "olive", "maroon", "aqua", "gold", "silver", "coral", "tomato", "salmon", "violet", "indigo", "turquoise", "beige", "crimson", "khaki"]

# ==============================
# CLASSE FORMAS GEOMÉTRICAS
# ==============================

class FormasGeometricas:
    def __init__(self, nome: str, tipo: str, pontos: list, qtd_lados: int, cor: str):
        self.nome = nome   
        self.tipo = tipo   
        self.pontos = pontos
        self.qtd_lados = qtd_lados
        self.cor = cor

    # ==============================
    # É desenhado na tela as figuras

    def adiconar_na_tela(self, canvas: tk.Canvas, vp: ViewPoint):
        if self.tipo == "ponto":
            x, y = self.pontos[0]
            xvp, yvp = vp.transformadaDeViewPoint(x, y)
            canvas.create_line(xvp, yvp, xvp+1, yvp, fill=self.cor)
        elif self.tipo == "linha":
            x1, y1 = self.pontos[0]
            x2, y2 = self.pontos[1]
            x1vp, y1vp = vp.transformadaDeViewPoint(x1, y1)
            x2vp, y2vp = vp.transformadaDeViewPoint(x2, y2)
            canvas.create_line(x1vp, y1vp, x2vp, y2vp, fill=self.cor)
        else:
            for j in range(len(self.pontos) - 1):
                xvp1, yvp1 = vp.transformadaDeViewPoint(self.pontos[j][0], self.pontos[j][1])
                xvp2, yvp2 = vp.transformadaDeViewPoint(self.pontos[j+1][0], self.pontos[j+1][1])
                canvas.create_line(xvp1, yvp1, xvp2, yvp2, fill=self.cor)           
            xvp1, yvp1 = vp.transformadaDeViewPoint(self.pontos[-1][0], self.pontos[-1][1])
            xvp2, yvp2 = vp.transformadaDeViewPoint(self.pontos[0][0], self.pontos[0][1])
            canvas.create_line(xvp1, yvp1, xvp2, yvp2, fill=self.cor)

    # =======================================================================
    # TRANSFORMAÇÕES DOS POLÍGONOS (TRANSLAÇÃO, ROTAÇÃO E ESCALONAMENTO)
    # =======================================================================

    def centro_poligono(self):
        soma_x = sum(ponto[0] for ponto in self.pontos)
        soma_y = sum(ponto[1] for ponto in self.pontos)
        qtd = len(self.pontos)

        return (soma_x / qtd, soma_y / qtd)

    def multiplicacao_matrizes(M1, M2):
        qtd_linha_M1 = len(M1)
        qtd_coluna_M1 = len(M1[0])
        qtd_coluna_M2 = len(M2[0])
        resultado = [[0] * qtd_coluna_M2 for _ in range(qtd_linha_M1)]

        for i in range(qtd_linha_M1):
            for j in range(qtd_coluna_M2):
                for k in range(qtd_coluna_M1):
                    resultado[i][j] += (M1[i][k] * M2[k][j])

        return resultado
    
    def fazer_matriz_translacao(self, dx, dy):
        return [[1, 0, 0],[0, 1, 0],[dx, dy, 1]]

    def fazer_matriz_rotacao_centro_mundo(self, angulo_graus):
        angulo = math.radians(angulo_graus)
        cosseno_angulo = math.cos(angulo)
        seno_angulo = math.sin(angulo)

        return [[cosseno_angulo, seno_angulo, 0],[-seno_angulo, cosseno_angulo, 0],[0, 0, 1]]

    def fazer_matriz_rotacao_centro_objeto(self,angulo_graus, x_centro, y_centro):
        angulo = math.radians(angulo_graus)
        cosseno_angulo = math.cos(angulo)
        seno_angulo = math.sin(angulo)
        matriz_rotacao = [[cosseno_angulo, seno_angulo, 0],[-seno_angulo, cosseno_angulo, 0],[0, 0, 1]]
        matriz_ida = [[1, 0, 0],[0, 1, 0],[-x_centro, -y_centro, 1]]
        matriz_volta = [[1, 0, 0],[0, 1, 0],[x_centro, y_centro, 1]]

        matriz_intermediaria = (FormasGeometricas.multiplicacao_matrizes(matriz_ida,matriz_rotacao))
        matriz_final = (FormasGeometricas.multiplicacao_matrizes(matriz_intermediaria,matriz_volta))

        return matriz_final

    def fazer_matriz_rotacao_ponto_arbritario(self, angulo_graus,x,y):
        angulo = math.radians(angulo_graus)
        cosseno_angulo = math.cos(angulo)
        seno_angulo = math.sin(angulo)
        matriz_rotacao = [[cosseno_angulo, seno_angulo, 0],[-seno_angulo, cosseno_angulo, 0],[0, 0, 1]]
        matriz_ida = [[1, 0, 0],[0, 1, 0],[-x, -y, 1]]
        matriz_volta = [[1, 0, 0],[0, 1, 0],[x, y, 1]]

        matriz_intermediaria = (FormasGeometricas.multiplicacao_matrizes(matriz_ida,matriz_rotacao))
        matriz_final = (FormasGeometricas.multiplicacao_matrizes(matriz_intermediaria,matriz_volta))

        return matriz_final

    def fazer_matriz_escalonamento(self, Sx, Sy, x_centro, y_centro):
        matriz_ida = [[1, 0, 0],[0, 1, 0],[-x_centro, -y_centro, 1]]
        matriz_escalonamento = [[Sx, 0, 0],[0, Sy, 0],[0, 0, 1]]
        matriz_volta = [[1, 0, 0],[0, 1, 0],[x_centro, y_centro, 1]]
        matriz_intermediaria = FormasGeometricas.multiplicacao_matrizes(matriz_ida,matriz_escalonamento)

        return FormasGeometricas.multiplicacao_matrizes(matriz_intermediaria,matriz_volta)

    def aplicar_matriz_transformacao(self,matriz_composta):
        novos_pontos = []
        for x, y in self.pontos:
            ponto_matriz = [[x, y, 1]]
            resultado = (FormasGeometricas.multiplicacao_matrizes(ponto_matriz,matriz_composta))
            novos_pontos.append((resultado[0][0],resultado[0][1]))
        self.pontos = novos_pontos

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
        return cls(nome, "ponto", pontos, 0, cor)

    @classmethod
    def drawCircle(cls, nome: str, cx: float, cy: float, raio: float, cor: str = None):
        if cor is None:
            cor = random.choice(cores)
        pontos = []
        for i in range(720):
            x = cx + raio * math.cos(2 * math.pi * i / 360)
            y = cy + raio * math.sin(2 * math.pi * i / 360)
            pontos.append((x, y))
        return cls(nome, "circulo", pontos, 1, cor)

    @classmethod
    def drawLine(cls, nome: str, x1: float, y1: float, x2: float, y2: float, cor: str = None):
        if cor is None:
            cor = random.choice(cores)
        pontos = [(x1, y1), (x2, y2)]
        return cls(nome, "linha", pontos, 0, cor)

    @classmethod
    def drawSquere(cls, nome: str, xi: float, yi: float, tamanho: float, cor: str = None):
        if cor is None:
            cor = random.choice(cores)
        pontos = [(xi, yi), (xi + tamanho, yi), (xi + tamanho, yi + tamanho), (xi, yi + tamanho)]    
        return cls(nome, "quadrado", pontos, 4, cor)

    @classmethod
    def drawWireframe(cls, nome: str, pontos: list, cor: str = None):
        if cor is None:
            cor = random.choice(cores)
        return cls(nome, "wireframe", pontos, len(pontos), cor)