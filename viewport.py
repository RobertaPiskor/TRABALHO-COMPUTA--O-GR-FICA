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
        self.transformador = TransformarObjetos()

    # ==========================================
    # Fórmula para calcular onde cada ponto vai 

    def transformadaDeViewPoint(self, xw: float, yw: float):
        xvp = ((xw - self.topleftX) / (self.bottomrightX - self.topleftX)) * (self.xvpmax - self.xvpmin)
        yvp = (1 - ((yw - self.topleftY)/ (self.bottomrightY - self.topleftY))) * (self.yvpmax - self.yvpmin)
        return int(xvp), int(yvp)

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

    # ==========================================
    # Fórmula para calcular onde cada ponto vai 

    def mundo_para_SCN(self, pontos):
        Wcx = (self.topleftX + self.bottomrightX) / 2.0
        Wcy = (self.topleftY + self.bottomrightY) / 2.0
        matriz_translacao = self.transformador.fazer_matriz_translacao(-Wcx,-Wcy)
        matriz_rotacao = self.transformador.fazer_matriz_rotacao_centro_mundo(-self.angulo_vup)

        largura_w = self.bottomrightX - self.topleftX
        altura_w = self.bottomrightY - self.topleftY

        sx = 2.0 / largura_w
        sy = 2.0 / altura_w

        matriz_escalonamento = [[sx, 0, 0],[0, sy, 0],[0, 0, 1]]

        matriz_intermediaria = self.transformador.multiplicacao_matrizes(matriz_translacao,matriz_rotacao)
        matriz_final = self.transformador.multiplicacao_matrizes(matriz_intermediaria,matriz_escalonamento)
        return self.transformador.aplicar_matriz_transformacao(pontos,matriz_final)

    def SCN_para_viewport(self, pontos_scn):
        pontos_tela = []
        for x_scn, y_scn in pontos_scn:
            xvp = (((x_scn + 1.0) / 2.0)*(self.xvpmax - self.xvpmin)+ self.xvpmin)
            yvp = ((1.0 - ((y_scn + 1.0) / 2.0))* (self.yvpmax - self.yvpmin)+ self.yvpmin)
            pontos_tela.append((int(xvp), int(yvp)))
        return pontos_tela

    def normalizacao(self, pontos_coordenadas_cartesianas):
        pontos_scn = self.mundo_para_SCN(pontos_coordenadas_cartesianas)
        pontos_tela = self.SCN_para_viewport(pontos_scn)
        return pontos_tela