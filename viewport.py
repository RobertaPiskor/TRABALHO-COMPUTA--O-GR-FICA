from transfromadas_objetos import TransformarObjetos
import math

# ==============================
# CLASSE VIEWPOINT
# ==============================

class ViewPoint:
    # ====================
    # Variáveis de Estado    

    def __init__(self, largura=600, altura=600):
        self.xvpmin = 10
        self.xvpmax = largura - 10
        self.yvpmin = 10
        self.yvpmax = altura - 10

        self.topleftX = -largura / 2
        self.topleftY = -altura / 2
        self.bottomrightX = largura / 2
        self.bottomrightY = altura / 2

        self.angulo_vup = 0.0

        self.clipping =  "Cohen-Sutherland"
        
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
        radiano = math.radians(self.angulo_vup)
        self.topleftX += 10 * math.cos(radiano)
        self.bottomrightX += 10 * math.cos(radiano)
        self.topleftY += 10 * math.sin(radiano)
        self.bottomrightY += 10 * math.sin(radiano)

    def left(self):
        radiano = math.radians(self.angulo_vup)
        self.topleftX -= 10 * math.cos(radiano)
        self.bottomrightX -= 10 * math.cos(radiano)
        self.topleftY -= 10 * math.sin(radiano)
        self.bottomrightY -= 10 * math.sin(radiano)

    def up(self):
        radiano = math.radians(self.angulo_vup)
        self.topleftX -= 10 * math.sin(radiano)
        self.bottomrightX -= 10 * math.sin(radiano)
        self.topleftY += 10 * math.cos(radiano)
        self.bottomrightY += 10 * math.cos(radiano)

    def down(self):
        radiano = math.radians(self.angulo_vup)
        self.topleftX += 10 * math.sin(radiano)
        self.bottomrightX += 10 * math.sin(radiano)
        self.topleftY -= 10 * math.cos(radiano)
        self.bottomrightY -= 10 * math.cos(radiano)

    # ====================================================================================================
    # Fórmula para calcular onde cada ponto vai (fazer a normalização). pega do mundo -> SCN -> viewpoint

    def RealizarNormalizacao(self, pontos, tipo_forma):
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
        pontos_scn = transformador.aplicar_matriz_transformacao(pontos, matriz_final)

        pontos_clipados = self.aplicar_clipping(pontos_scn, tipo_forma)

        if not pontos_clipados:
            return []

        for x_scn, y_scn in pontos_clipados:
            xvp = (((x_scn + 1) / 2) * (self.xvpmax - self.xvpmin)+ self.xvpmin)
            yvp = ((1 - ((y_scn + 1) / 2)) * (self.yvpmax - self.yvpmin)+ self.yvpmin)
            posicao_pontos_tela.append((int(xvp), int(yvp)))

        return posicao_pontos_tela

    # ===================
    # realizar clipping

    def aplicar_clipping(self, pontos_scn, tipo_forma):
        if len(pontos_scn) == 0:
            return []

        if tipo_forma == "ponto":
            x, y = pontos_scn[0]
            if -1.0 <= x <= 1.0 and -1.0 <= y <= 1.0:
                return pontos_scn
            return []
        elif tipo_forma == "linha":
            if self.clipping == "Cohen-Sutherland":
                return self.clip_linha_cohen_sutherland(pontos_scn[0], pontos_scn[1])
            elif self.clipping == "Liang-Barsky":
                return self.clip_linha_liang_barsky(pontos_scn[0], pontos_scn[1])
        else: 
            return self.clip_poligono_sutherland_hodgeman(pontos_scn)

    def calcular_codigo_regiao(self, x, y):
        regiao_ponto = [0, 0, 0, 0]
        if x < -1:
            regiao_ponto[3] = 1  
        else:
            regiao_ponto[3] = 0
        if x > 1:
            regiao_ponto[2] = 1  
        else:
            regiao_ponto[2] = 0
        if y < -1:
            regiao_ponto[1] = 1  
        else:
            regiao_ponto[1] = 0
        if y > 1:
            regiao_ponto[0] = 1 
        else:
            regiao_ponto[0] = 0
        return regiao_ponto

    def clip_linha_cohen_sutherland(self, p1, p2):
        x1, y1 = p1
        x2, y2 = p2

        while True:
            regiao_p1 = self.calcular_codigo_regiao(x1, y1)
            regiao_p2 = self.calcular_codigo_regiao(x2, y2)

            if sum(regiao_p1) == 0 and sum(regiao_p2) == 0:
                return [(x1, y1), (x2, y2)]   

            elif (regiao_p1[0] == 1 and regiao_p2[0] == 1) or (regiao_p1[1] == 1 and regiao_p2[1] == 1) or (regiao_p1[2] == 1 and regiao_p2[2] == 1) or (regiao_p1[3] == 1 and regiao_p2[3] == 1):
                return []  

            else:
                x_intersecao = 0.0
                y_intersecao = 0.0

                if x2 != x1:
                    m = (y2 - y1) / (x2 - x1)
                else:
                    m = None 

                if sum(regiao_p1) > 0:
                    regiao_fora = regiao_p1
                    x_fora = x1
                    y_fora = y1
                    ponto_fora = "p1"
                else:
                    regiao_fora = regiao_p2
                    x_fora = x2
                    y_fora = y2
                    ponto_fora = "p2"

                if regiao_fora[0] == 1:
                    y_intersecao = 1.0
                    if m != None and m != 0:
                        x_intersecao = x_fora + (1/m) * (1.0 - y_fora)
                    else:
                        x_intersecao = x_fora

                elif regiao_fora[1] == 1:
                    y_intersecao = -1.0
                    if m != None and m != 0:
                        x_intersecao = x_fora + (1/m) * (-1.0 - y_fora)
                    else:
                        x_intersecao = x_fora

                elif regiao_fora[2] == 1:
                    x_intersecao = 1.0
                    y_intersecao = m * (1.0 - x_fora) + y_fora

                elif regiao_fora[3] == 1:
                    x_intersecao = -1.0
                    y_intersecao = m * (-1.0 - x_fora) + y_fora

                if ponto_fora == "p1":
                    x1 = x_intersecao
                    y1 = y_intersecao
                else:
                    x2 = x_intersecao
                    y2 = y_intersecao

    def clip_linha_liang_barsky(self, ponto1, ponto2):
        x1, y1 = ponto1
        x2, y2 = ponto2

        delta_x = x2 - x1
        delta_y = y2 - y1

        p = [-delta_x, delta_x, -delta_y, delta_y]
        q = [x1+1, 1-x1, y1+1, 1-y1]

        t1 = 0.0
        t2 = 1.0

        for k in range(4):
            if p[k] == 0:
                if q[k] < 0:
                    return []            
            else:
                r = q[k] / p[k]                
                if p[k] < 0:
                    t1 = max(t1, r)
                elif p[k] > 0:
                    t2 = min(t2, r)
        if t1 > t2:
            return []
        
        return [((x1 + t1 * delta_x), (y1 + t1 * delta_y)), ((x1 + t2 * delta_x), (y1 + t2 * delta_y))]

    # ================================================
    # OBSERVAÇÃO: Escolhemos esse algorítimo visto que foi o mais falado em aula de poliginos
    # Pensamos em usar como principal base o "pseudo-código" de
    # https://www.sunshine2k.de/coding/java/SutherlandHodgman/SutherlandHodgman.html

    def clip_poligono_sutherland_hodgeman(self, pontos_poligono):
        if not pontos_poligono or len(pontos_poligono) < 3:
            return []

        poligono_atual = pontos_poligono

        for qual_borda in range(4):
            poligono_recortado = []
            tamanho = len(poligono_atual)
            if tamanho == 0:
                break
            for j in range(tamanho): 
                x1, y1 = poligono_atual[j]
                x2, y2 = poligono_atual[(j + 1) % tamanho]                       
                regiao_p1 = self.calcular_codigo_regiao(x1, y1)
                regiao_p2 = self.calcular_codigo_regiao(x2, y2)

                p1_dentro = (regiao_p1[qual_borda] == 0)
                p2_dentro = (regiao_p2[qual_borda] == 0)

                if p1_dentro:
                    if p2_dentro:
                        poligono_recortado.append((x2, y2))
                    else:
                        ponto_intersecao = self.calcular_intersecao(x1, y1, x2, y2, qual_borda)
                        poligono_recortado.append(ponto_intersecao)
                else:
                    if p2_dentro:
                        ponto_intersecao = self.calcular_intersecao(x1, y1, x2, y2, qual_borda)
                        poligono_recortado.append(ponto_intersecao)
                        poligono_recortado.append((x2, y2))
            
            poligono_atual = poligono_recortado

        return poligono_atual

    def calcular_intersecao(self, x1, y1, x2, y2, qual_borda):
        dx = x2 - x1
        dy = y2 - y1

        if qual_borda == 3: 
            x = -1.0
            if dx != 0:
                y = y1 + dy * (-1.0 - x1) / dx
            else:
                y = y1

        elif qual_borda == 2: 
            x = 1.0
            if dx != 0:
                y = y1 + dy * (1.0 - x1) / dx
            else:
                y = y1

        elif qual_borda == 1: 
            y = -1.0
            if dy != 0:
                x = x1 + dx * (-1.0 - y1) / dy
            else:
                x = x1

        elif qual_borda == 0: 
            y = 1.0
            if dy != 0:
                x = x1 + dx * (1.0 - y1) / dy
            else:
                x = x1

        return (x, y)