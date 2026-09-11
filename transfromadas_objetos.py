import math

class TransformarObjetos:

    # ============================
    # Encontra centro do polígono

    def centro_poligono(self, pontos):
        soma_x = 0
        soma_y = 0
        for ponto in pontos:
            soma_x += ponto[0]
            soma_y += ponto[1]
        qtd = len(pontos)
        return (soma_x / qtd, soma_y / qtd)

    # ===================================
    # Multiplicação genérica de matrizes

    def multiplicacao_matrizes(self, M1, M2):
        qtd_linha_M1 = len(M1)
        qtd_coluna_M1 = len(M1[0])
        qtd_coluna_M2 = len(M2[0])
        resultado = []
        for i in range(qtd_linha_M1):
            linha = []
            for j in range(qtd_coluna_M2):
                linha.append(0)
            resultado.append(linha)
        for i in range(qtd_linha_M1):
            for j in range(qtd_coluna_M2):
                for k in range(qtd_coluna_M1):
                    resultado[i][j] += M1[i][k] * M2[k][j]
        return resultado

    # =====================================
    # MATRIZES DE TRANSFORMAÇÃO (GENÉRICO)

    def fazer_matriz_translacao(self, dx, dy):
        return [[1, 0, 0],[0, 1, 0],[dx, dy, 1]]

    def fazer_matriz_rotacao_centro_mundo(self, angulo_graus):
        angulo = math.radians(angulo_graus)
        cosseno_angulo = math.cos(angulo)
        seno_angulo = math.sin(angulo)
        return [[cosseno_angulo, seno_angulo, 0],[-seno_angulo, cosseno_angulo, 0],[0, 0, 1]]

    def fazer_matriz_rotacao_centro_objeto(self, angulo_graus, x_centro, y_centro):
        angulo = math.radians(angulo_graus)

        cosseno_angulo = math.cos(angulo)
        seno_angulo = math.sin(angulo)

        matriz_rotacao = [[cosseno_angulo, seno_angulo, 0],[-seno_angulo, cosseno_angulo, 0],[0, 0, 1]]
        matriz_ida = [[1, 0, 0],[0, 1, 0],[-x_centro, -y_centro, 1]]
        matriz_volta = [[1, 0, 0],[0, 1, 0],[x_centro, y_centro, 1]]

        matriz_intermediaria = self.multiplicacao_matrizes(matriz_ida, matriz_rotacao)
        matriz_final = self.multiplicacao_matrizes(matriz_intermediaria, matriz_volta)

        return matriz_final

    def fazer_matriz_rotacao_ponto_arbritario(self, angulo_graus, x, y):
        angulo = math.radians(angulo_graus)

        cosseno_angulo = math.cos(angulo)
        seno_angulo = math.sin(angulo)

        matriz_rotacao = [[cosseno_angulo, seno_angulo, 0],[-seno_angulo, cosseno_angulo, 0],[0, 0, 1]]
        matriz_ida = [[1, 0, 0],[0, 1, 0],[-x, -y, 1]]
        matriz_volta = [[1, 0, 0],[0, 1, 0],[x, y, 1]]

        matriz_intermediaria = self.multiplicacao_matrizes(matriz_ida, matriz_rotacao)
        matriz_final = self.multiplicacao_matrizes(matriz_intermediaria, matriz_volta)

        return matriz_final

    def fazer_matriz_escalonamento(self, Sx, Sy, x_centro, y_centro):
        matriz_ida = [[1, 0, 0],[0, 1, 0],[-x_centro, -y_centro, 1]]
        matriz_escalonamento = [[Sx, 0, 0],[0, Sy, 0],[0, 0, 1]]
        matriz_volta = [[1, 0, 0],[0, 1, 0],[x_centro, y_centro, 1]]

        matriz_intermediaria = self.multiplicacao_matrizes(matriz_ida, matriz_escalonamento)

        return self.multiplicacao_matrizes(matriz_intermediaria, matriz_volta)

    # ==============================
    # Aplicar as matrizes nos pontos

    def aplicar_matriz_transformacao(self, pontos, matriz_composta):
        novos_pontos = []
        for x, y in pontos:
            ponto_matriz = [[x, y, 1]]
            resultado = self.multiplicacao_matrizes(ponto_matriz, matriz_composta)
            novos_pontos.append((resultado[0][0], resultado[0][1]))
        return novos_pontos