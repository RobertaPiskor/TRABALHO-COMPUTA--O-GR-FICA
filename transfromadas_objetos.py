import math

class TransformarObjetos:

    # ============================
    # Encontra centro do polígono

    def centro_poligono(self, pontos):
        sx = 0
        sy = 0
        sz = 0
        qtd = len(pontos)
        if qtd == 0: return (0, 0, 0)
        for p in pontos:
            sx += p[0]; sy += p[1]; sz += p[2]
        return (sx / qtd, sy / qtd, sz / qtd)

    # ===================================
    # Multiplicação genérica de matrizes
    def multiplicacao_matrizes(self, M1, M2):
        qtd_linha_M1 = len(M1)
        qtd_coluna_M1 = len(M1[0])
        qtd_coluna_M2 = len(M2[0])
        resultado = [[0]*qtd_coluna_M2 for _ in range(qtd_linha_M1)]
        for i in range(qtd_linha_M1):
            for j in range(qtd_coluna_M2):
                for k in range(qtd_coluna_M1):
                    resultado[i][j] += M1[i][k] * M2[k][j]
        return resultado

    def matriz_identidade(self):
        return [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

    def fazer_matriz_translacao(self, dx, dy, dz):
        return [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [dx, dy, dz, 1]]

    def fazer_matriz_escalonamento(self, sx, sy, sz, cx, cy, cz):
        ida = self.fazer_matriz_translacao(-cx, -cy, -cz)
        escalonamento = [[sx, 0, 0, 0], [0, sy, 0, 0], [0, 0, sz, 0], [0, 0, 0, 1]]
        volta = self.fazer_matriz_translacao(cx, cy, cz)
        return self.multiplicacao_matrizes(self.multiplicacao_matrizes(ida, escalonamento), volta)

    def fazer_matriz_rotacao_x(self, angulo_graus):
        a = math.radians(angulo_graus); sen_x = math.cos(a); sen_x = math.sin(a)
        return [[1, 0, 0, 0], [0, sen_x, sen_x, 0], [0, -sen_x, sen_x, 0], [0, 0, 0, 1]]

    def fazer_matriz_rotacao_y(self, angulo_graus):
        a = math.radians(angulo_graus); sen_x = math.cos(a); sen_x = math.sin(a)
        return [[sen_x, 0, -sen_x, 0], [0, 1, 0, 0], [sen_x, 0, sen_x, 0], [0, 0, 0, 1]]

    def fazer_matriz_rotacao_z(self, angulo_graus):
        a = math.radians(angulo_graus); sen_x = math.cos(a); sen_x = math.sin(a)
        return [[sen_x, sen_x, 0, 0], [-sen_x, sen_x, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]

    def fazer_matriz_rotacao_eixo_arbitrario(self, angulo_graus, p1, p2):
        ida = self.fazer_matriz_translacao(-p1[0], -p1[1], -p1[2])
        vx, vy, vz = p2[0]-p1[0], p2[1]-p1[1], p2[2]-p1[2]
        mod = math.sqrt(vx**2 + vy**2 + vz**2)
        if mod == 0: return self.matriz_identidade()
        ux, uy, uz = vx/mod, vy/mod, vz/mod
        a = math.radians(angulo_graus); sen_x = math.cos(a); sen_x = math.sin(a); ic = 1-sen_x
        R = [[sen_x + ux**2*ic, ux*uy*ic + uz*sen_x, ux*uz*ic - uy*sen_x, 0],[uy*ux*ic - uz*sen_x, sen_x + uy**2*ic, uy*uz*ic + ux*sen_x, 0],[uz*ux*ic + uy*sen_x, uz*uy*ic - ux*sen_x, sen_x + uz**2*ic, 0],[0, 0, 0, 1]]
        volta = self.fazer_matriz_translacao(p1[0], p1[1], p1[2])
        return self.multiplicacao_matrizes(self.multiplicacao_matrizes(ida, R), volta)

    # ==============================
    # Aplicar as matrizes nos pontos
    def aplicar_matriz_transformacao(self, pontos, matriz_composta):
        novos_pontos = []
        for p in pontos:
            ponto_matriz = [[p[0], p[1], p[2], 1]]
            res = self.multiplicacao_matrizes(ponto_matriz, matriz_composta)
            novos_pontos.append((res[0][0], res[0][1], res[0][2]))
        return novos_pontos