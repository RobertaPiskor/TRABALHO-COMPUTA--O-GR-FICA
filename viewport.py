from transfromadas_objetos import TransformarObjetos

# ==============================
# CLASSE VIEWPOINT
# ==============================

class ViewPoint:
    # ====================
    # Variáveis de Estado    

    def __init__(self, largura=600, altura=600):
        self.xvpmin = 0
        self.xvpmax = largura
        self.yvpmin = 0
        self.yvpmax = altura

        self.topleftX = -largura / 2
        self.topleftY = -altura / 2
        self.bottomrightX = largura / 2
        self.bottomrightY = altura / 2

        self.angulo_vup = 0.0

    # ====================================================================
    # Métodos que executam o que deve fazer quando se é apertado um botão 

    def rotacao_window(self, angulo: float):
        self.angulo_vup = (self.angulo_vup + angulo) % 360.0

    def zoomIn(self):
        self.topleftX, self.bottomrightX = self.topleftX + (self.bottomrightX - self.topleftX) * 0.1, self.bottomrightX - (self.bottomrightX - self.topleftX) * 0.1
        self.topleftY, self.bottomrightY = self.topleftY + (self.bottomrightY - self.topleftY) * 0.1, self.bottomrightY - (self.bottomrightY - self.topleftY) * 0.1

    def zoomOut(self):
        self.topleftX, self.bottomrightX = self.topleftX - (self.bottomrightX - self.topleftX) * 0.1, self.bottomrightX + (self.bottomrightX - self.topleftX) * 0.1
        self.topleftY, self.bottomrightY = self.topleftY - (self.bottomrightY - self.topleftY) * 0.1, self.bottomrightY + (self.bottomrightY - self.topleftY) * 0.1

    def right(self):
        self.topleftX += 10
        self.bottomrightX += 10

    def left(self):
        self.topleftX -= 10
        self.bottomrightX -= 10

    def down(self):
        self.topleftY -= 10
        self.bottomrightY -= 10

    def up(self):
        self.topleftY += 10
        self.bottomrightY += 10

    # ====================================================================================================
    # Fórmula para calcular onde cada ponto vai (fazer a normailização). pega do mundo -> SCN -> vierpoint

    def RealizarNormalizacao(self, pontos):
        transformador = TransformarObjetos()

        posicao_pontos_tela = []
        Wcx = (self.topleftX + self.bottomrightX) / 2.0
        Wcy = (self.topleftY + self.bottomrightY) / 2.0
        matriz_translacao = transformador.fazer_matriz_translacao(-Wcx,-Wcy)
        matriz_rotacao = transformador.fazer_matriz_rotacao_centro_mundo(-self.angulo_vup)

        sx = 2.0 / (self.bottomrightX - self.topleftX)
        sy = 2.0 / (self.bottomrightY - self.topleftY)

        matriz_escalonamento = transformador.fazer_matriz_escalonamento(sx, sy, 0, 0)

        matriz_intermediaria = transformador.multiplicacao_matrizes(matriz_translacao, matriz_rotacao)
        matriz_final = transformador.multiplicacao_matrizes(matriz_intermediaria, matriz_escalonamento)
        pontos_trasnformados_scn = transformador.aplicar_matriz_transformacao(pontos, matriz_final)

        for x_scn, y_scn in pontos_trasnformados_scn:
            xvp = (((x_scn + 1) / 2) * (self.xvpmax - self.xvpmin)+ self.xvpmin)
            yvp = ((1 - ((y_scn + 1) / 2)) * (self.yvpmax - self.yvpmin)+ self.yvpmin)
            posicao_pontos_tela.append((int(xvp), int(yvp)))

        return posicao_pontos_tela