
# ==============================
# CLASSE VIEWPOINT
# ==============================

class ViewPoint:
    # ==============================
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

    # ==============================
    # Fórmula para calcular onde cada ponto vai 

    def transformadaDeViewPoint(self, xw: float, yw: float):
        xvp = ((xw - self.topleftX) / (self.bottomrightX - self.topleftX)) * (self.xvpmax - self.xvpmin)
        yvp = (1 - ((yw - self.topleftY)/ (self.bottomrightY - self.topleftY))) * (self.yvpmax - self.yvpmin)
        return int(xvp), int(yvp)

    # ==============================
    # Métodos que executam o que deve fazer quando se é apertado um botão 

    def zoomIn(self):
        self.topleftX, self.bottomrightX = self.topleftX + (self.bottomrightX - self.topleftX) * 0.1, self.bottomrightX - (self.bottomrightX - self.topleftX) * 0.1
        self.topleftY, self.bottomrightY = self.topleftY + (self.bottomrightY - self.topleftY) * 0.1, self.bottomrightY - (self.bottomrightY - self.topleftY) * 0.1

    def zoomOut(self):
        self.topleftX, self.bottomrightX = self.topleftX - (self.bottomrightX - self.topleftX) * 0.1, self.bottomrightX + (self.bottomrightX - self.topleftX) * 0.1
        self.topleftY, self.bottomrightY = self.topleftY - (self.bottomrightY - self.topleftY) * 0.1, self.bottomrightY + (self.bottomrightY - self.topleftY) * 0.1

    def right(self):
        self.topleftX -= 10
        self.bottomrightX -= 10

    def left(self):
        self.topleftX += 10
        self.bottomrightX += 10

    def down(self):
        self.topleftY += 10
        self.bottomrightY += 10

    def up(self):
        self.topleftY -= 10
        self.bottomrightY -= 10

