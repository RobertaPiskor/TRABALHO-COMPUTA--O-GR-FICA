import math
import random
import tkinter as tk
from viewport import ViewPoint
from transfromadas_objetos import TransformarObjetos

cores = ["#ff0000", "#bb00ff", "#008000", "#ffff00", "#ffa500", "#800080", "#ffc0cb", "#a52a2a", "#000000", "#ffffff", "#808080", "#00ffff", "#ff00ff", "#00ff00", "#000080", "#008080", "#808000", "#800000", "#00ffff", "#ffd700", "#c0c0c0", "#ff7f50", "#ff6347", "#fa8072", "#ee82ee", "#4b0082", "#40e0d0", "#f5f5dc", "#dc143c", "#f0e68c"]

class FormaCurva:
    def __init__(self, nome: str, pontos: list, cor: str):
        self.nome = nome
        self.tipo = "curva"         
        self.pontos_controle = pontos         
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