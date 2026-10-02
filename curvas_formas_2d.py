import math
import random
import tkinter as tk
from viewport import ViewPoint
from transfromadas_objetos import TransformarObjetos

cores = ["#ff0000", "#bb00ff", "#008000", "#ffff00", "#ffa500", "#800080", "#ffc0cb", "#a52a2a", "#000000", "#ffffff", "#808080", "#00ffff", "#ff00ff", "#00ff00", "#000080", "#008080", "#808000", "#800000", "#00ffff", "#ffd700", "#c0c0c0", "#ff7f50", "#ff6347", "#fa8072", "#ee82ee", "#4b0082", "#40e0d0", "#f5f5dc", "#dc143c", "#f0e68c"]

class FormaCurva:
    def __init__(self, nome: str, pontos: list, cor: str, tipo_curva: str = "bezier"):
        self.nome = nome
        self.tipo = "curva"         
        self.pontos_controle = pontos
        self.tipo_curva = tipo_curva        
        if self.tipo_curva == "bspline":
            self.pontos = self.calcular_b_splines_com_Forward_differences(self.pontos_controle)
        else:
            self.pontos = self.calcular_curva_bezier(self.pontos_controle)
        if cor is None:
            self.cor = random.choice(cores)
        else:
            self.cor = cor
    def calcular_curva_bezier(self, pontos_controle):
        transformador = TransformarObjetos()
        pontos_gerados = []
        
        matriz_de_bezier = [[-1,  3, -3,  1],[ 3, -6,  3,  0],[-3,  3,  0,  0],[ 1,  0,  0,  0]]
        
        for i in range(0, len(pontos_controle) - 3, 3):
            matriz_de_geometria = [[pontos_controle[i][0],pontos_controle[i][1]],[pontos_controle[i+1][0], pontos_controle[i+1][1]],[pontos_controle[i+2][0], pontos_controle[i+2][1]],[pontos_controle[i+3][0], pontos_controle[i+3][1]]]   
            for j in range(101):
                t = j / 100
                vetor_parametrico = [[t**3, t**2, t, 1]] 
                resultado_TM = transformador.multiplicacao_matrizes(vetor_parametrico, matriz_de_bezier)
                resultado_xy = transformador.multiplicacao_matrizes(resultado_TM, matriz_de_geometria)
                x = resultado_xy[0][0]
                y = resultado_xy[0][1]
                pontos_gerados.append((x, y))
                
        return pontos_gerados

    def desenhar_curva_fwd_diff(self, n, x, dx, ddx, dddx, y, dy, ddy, dddy):
        pontos_segmento = []
        i = 1
        x_velho = x
        y_velho = y
        pontos_segmento.append((x_velho, y_velho))
        
        while i < n:
            i += 1
            
            x = x + dx 
            dx = dx + ddx 
            ddx = ddx + dddx
            
            y = y + dy 
            dy = dy + ddy 
            ddy = ddy + dddy
            
            pontos_segmento.append((x, y))
            
            x_velho = x
            y_velho = y
            
        return pontos_segmento


    def calcular_b_splines_com_Forward_differences(self, pontos_controle):
        transformador = TransformarObjetos()
        pontos_gerados = []
        
        Gx = []
        Gy = []
        for ponto in pontos_controle:
            Gx.append(ponto[0])
            Gy.append(ponto[1])

        MBS = [[-1/6, 1/2, -1/2,1/6],[1/2, -1, 1/2, 0],[-1/2,0,1/2,0],[1/6,2/3,1/6,0]]
        n = 100 
        delta = 1/n

        E = [[0, 0, 0, 1],[delta**3, delta**2, delta, 0],[6 * (delta**3), 2 * (delta**2), 0, 0],[6 * (delta**3), 0, 0, 0]]

        for i in range(len(pontos_controle) - 3):
            Gx = [[pontos_controle[i][0]], [pontos_controle[i+1][0]], [pontos_controle[i+2][0]], [pontos_controle[i+3][0]]]
            Gy = [[pontos_controle[i][1]], [pontos_controle[i+1][1]], [pontos_controle[i+2][1]], [pontos_controle[i+3][1]]]

            Cx = transformador.multiplicacao_matrizes(MBS, Gx)
            Cy = transformador.multiplicacao_matrizes(MBS, Gy)

            Dx = transformador.multiplicacao_matrizes(E, Cx)
            Dy = transformador.multiplicacao_matrizes(E, Cy)

            x, dx, ddx, dddx = Dx[0][0], Dx[1][0], Dx[2][0], Dx[3][0]
            y, dy, ddy, dddy = Dy[0][0], Dy[1][0], Dy[2][0], Dy[3][0]

            pontos_do_segmento = self.desenhar_curva_fwd_diff(n, x, dx, ddx, dddx, y, dy, ddy, dddy)
            pontos_gerados.extend(pontos_do_segmento)

        return pontos_gerados

    def adiconar_na_tela(self, canvas, viewport):
        posicao_pontos_tela = viewport.RealizarNormalizacao(self.pontos, self.tipo)        
        if not posicao_pontos_tela:
            return
        for i in range(len(posicao_pontos_tela) - 1):
            if posicao_pontos_tela[i] is None or posicao_pontos_tela[i+1] is None:
                continue
            x1, y1 = posicao_pontos_tela[i]
            x2, y2 = posicao_pontos_tela[i+1]
            canvas.create_line(x1, y1, x2, y2, fill=self.cor, width=1)