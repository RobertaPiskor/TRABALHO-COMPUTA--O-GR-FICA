import math
from transfromadas_objetos import TransformarObjetos

# ==============================
# CLASSE VIEWPOINT (CÂMERA 3D)
# ==============================

class ViewPoint:
    def __init__(self, largura=600, altura=600):
        self.xvpmin = 10
        self.xvpmax = largura - 10
        self.yvpmin = 10
        self.yvpmax = altura - 10

        self.window_width = float(largura)
        self.window_height = float(altura)

        self.vrp = [0.0, 0.0, 0.0]
        self.vpn = [0.0, 0.0, 1.0]  
        self.vup = [0.0, 1.0, 0.0]   

        self.clipping = "Cohen-Sutherland"
        self.d = 600.0
        self.observacao = "ortogonal"
    
    def calcular_vetores_uvn(self):
        mod_vpn = math.sqrt(self.vpn[0]**2 + self.vpn[1]**2 + self.vpn[2]**2)
        n = [0, 0, 0] if mod_vpn == 0 else [self.vpn[0]/mod_vpn, self.vpn[1]/mod_vpn, self.vpn[2]/mod_vpn]
        
        cx = self.vup[1]*n[2] - self.vup[2]*n[1]
        cy = self.vup[2]*n[0] - self.vup[0]*n[2]
        cz = self.vup[0]*n[1] - self.vup[1]*n[0]
        mod_u = math.sqrt(cx**2 + cy**2 + cz**2)
        u = [0, 0, 0] if mod_u == 0 else [cx/mod_u, cy/mod_u, cz/mod_u]
        
        vx = n[1]*u[2] - n[2]*u[1]
        vy = n[2]*u[0] - n[0]*u[2]
        vz = n[0]*u[1] - n[1]*u[0]
        mod_v = math.sqrt(vx**2 + vy**2 + vz**2)
        v = [0, 0, 0] if mod_v == 0 else [vx/mod_v, vy/mod_v, vz/mod_v]
        
        return u, v, n

    # ====================================================================
    # NAVEGAÇÃO DA WINDOW NO ESPAÇO 3D
    # ====================================================================

    def zoomIn(self):
        self.window_width *= 0.9
        self.window_height *= 0.9

    def zoomOut(self):
        self.window_width *= 1.1
        self.window_height *= 1.1

    def right(self):
        u, v, n = self.calcular_vetores_uvn()
        passo = 10.0
        self.vrp[0] += u[0] * passo
        self.vrp[1] += u[1] * passo
        self.vrp[2] += u[2] * passo

    def left(self):
        u, v, n = self.calcular_vetores_uvn()
        passo = 10.0
        self.vrp[0] -= u[0] * passo
        self.vrp[1] -= u[1] * passo
        self.vrp[2] -= u[2] * passo

    def up(self):
        u, v, n = self.calcular_vetores_uvn()
        passo = 10.0
        self.vrp[0] += v[0] * passo
        self.vrp[1] += v[1] * passo
        self.vrp[2] += v[2] * passo

    def down(self):
        u, v, n = self.calcular_vetores_uvn()
        passo = 10.0
        self.vrp[0] -= v[0] * passo
        self.vrp[1] -= v[1] * passo
        self.vrp[2] -= v[2] * passo

    def mapear_para_camera(self, pontos):
        transformador = TransformarObjetos()
        u, v, n = self.calcular_vetores_uvn()

        cop_x = self.vrp[0] + self.d * n[0]
        cop_y = self.vrp[1] + self.d * n[1]
        cop_z = self.vrp[2] + self.d * n[2]

        T = transformador.fazer_matriz_translacao(-cop_x, -cop_y, -cop_z)
        R = [[u[0], v[0], n[0], 0],[u[1], v[1], n[1], 0],[u[2], v[2], n[2], 0],[0,0,0, 1]]

        matriz_src = transformador.multiplicacao_matrizes(T, R)
        return transformador.aplicar_matriz_transformacao(pontos, matriz_src)
    
    def projetar_perspectiva(self, pontos_camera):
        pontos_projetados_2d = []
        for x, y, z in pontos_camera:
            prof = -z
            pontos_projetados_2d.append((self.d * x / prof, self.d * y / prof, 0.0))
        return pontos_projetados_2d

    def rotacao_window(self, angulo_graus):
        transformador = TransformarObjetos()
        M_rot = transformador.fazer_matriz_rotacao_eixo_arbitrario(angulo_graus, [0, 0, 0], self.vpn)
        novo_vup = transformador.aplicar_matriz_transformacao([[self.vup[0], self.vup[1], self.vup[2]]], M_rot)
        self.vup = [novo_vup[0][0], novo_vup[0][1], novo_vup[0][2]]
    
    def RealizarNormalizacao(self, pontos, tipo_forma):
        if self.observacao == "ortogonal":
            transformador = TransformarObjetos()

            T = transformador.fazer_matriz_translacao(-self.vrp[0], -self.vrp[1], -self.vrp[2])
            u, v, n = self.calcular_vetores_uvn()
            
            R = [[u[0], v[0], n[0], 0],[u[1], v[1], n[1], 0],[u[2], v[2], n[2], 0],[0,0,0, 1]]
            
            matriz_src = transformador.multiplicacao_matrizes(T, R)
            pontos_src = transformador.aplicar_matriz_transformacao(pontos, matriz_src)

            pontos_projetados_2d = [(p[0], p[1], 0.0) for p in pontos_src]

            sx = 2.0 / self.window_width
            sy = 2.0 / self.window_height
            matriz_escalonamento = transformador.fazer_matriz_escalonamento(sx, sy, 1.0, 0.0, 0.0, 0.0)        
            
            pontos_scn_3d = transformador.aplicar_matriz_transformacao(pontos_projetados_2d, matriz_escalonamento)
            
            pontos_scn = [(p[0], p[1]) for p in pontos_scn_3d]

            pontos_clipados = self.aplicar_clipping(pontos_scn, tipo_forma)

            if not pontos_clipados:
                return []

            posicao_pontos_tela = []
            for ponto in pontos_clipados:
                if ponto is None:
                    posicao_pontos_tela.append(None)
                else:
                    x_scn, y_scn = ponto
                    xvp = (((x_scn + 1) / 2) * (self.xvpmax - self.xvpmin) + self.xvpmin)
                    yvp = ((1 - ((y_scn + 1) / 2)) * (self.yvpmax - self.yvpmin) + self.yvpmin)
                    posicao_pontos_tela.append((int(xvp), int(yvp)))

            return posicao_pontos_tela
        else:
            pontos_camera = self.mapear_para_camera(pontos)
            pontos_projetados = self.projetar_perspectiva(pontos_camera)

            transformador = TransformarObjetos()
            sx = 2.0 / self.window_width
            sy = 2.0 / self.window_height
            matriz_escalonamento = transformador.fazer_matriz_escalonamento(sx, sy, 1.0, 0.0, 0.0, 0.0)        
            pontos_scn_3d = transformador.aplicar_matriz_transformacao(pontos_projetados, matriz_escalonamento)
            pontos_scn = [(p[0], p[1]) for p in pontos_scn_3d]

            pontos_clipados = self.aplicar_clipping(pontos_scn, tipo_forma)
            if not pontos_clipados:
                return []

            posicao_pontos_tela = []
            for ponto in pontos_clipados:
                if ponto is None:
                    posicao_pontos_tela.append(None)
                else:
                    x_scn, y_scn = ponto
                    xvp = (((x_scn + 1) / 2) * (self.xvpmax - self.xvpmin) + self.xvpmin)
                    yvp = ((1 - ((y_scn + 1) / 2)) * (self.yvpmax - self.yvpmin) + self.yvpmin)
                    posicao_pontos_tela.append((int(xvp), int(yvp)))

            return posicao_pontos_tela

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
        elif tipo_forma == "curva":
            pontos_curva_clipados = []            
            for i in range(len(pontos_scn) - 1):
                p1 = pontos_scn[i]
                p2 = pontos_scn[i+1]                
                if self.clipping == "Cohen-Sutherland":
                    linha_clipada = self.clip_linha_cohen_sutherland(p1, p2)
                elif self.clipping == "Liang-Barsky":
                    linha_clipada = self.clip_linha_liang_barsky(p1, p2)
                else:
                    linha_clipada = []                    
                if linha_clipada:
                    if pontos_curva_clipados and pontos_curva_clipados[-1] != linha_clipada[0]:
                         pontos_curva_clipados.append(None)
                    pontos_curva_clipados.append(linha_clipada[0])
                    pontos_curva_clipados.append(linha_clipada[1])
            return pontos_curva_clipados
        else: 
            return self.clip_poligono_sutherland_hodgeman(pontos_scn)

    def calcular_codigo_regiao(self, x, y):
        regiao_ponto = [0, 0, 0, 0]
        if x < -1: regiao_ponto[3] = 1  
        if x > 1: regiao_ponto[2] = 1  
        if y < -1: regiao_ponto[1] = 1  
        if y > 1: regiao_ponto[0] = 1 
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
                m = (y2 - y1) / (x2 - x1) if x2 != x1 else None 

                if sum(regiao_p1) > 0:
                    regiao_fora, x_fora, y_fora, ponto_fora = regiao_p1, x1, y1, "p1"
                else:
                    regiao_fora, x_fora, y_fora, ponto_fora = regiao_p2, x2, y2, "p2"

                if regiao_fora[0] == 1:
                    y_intersecao = 1.0
                    x_intersecao = x_fora + (1/m) * (1.0 - y_fora) if m != None and m != 0 else x_fora
                elif regiao_fora[1] == 1:
                    y_intersecao = -1.0
                    x_intersecao = x_fora + (1/m) * (-1.0 - y_fora) if m != None and m != 0 else x_fora
                elif regiao_fora[2] == 1:
                    x_intersecao = 1.0
                    y_intersecao = m * (1.0 - x_fora) + y_fora
                elif regiao_fora[3] == 1:
                    x_intersecao = -1.0
                    y_intersecao = m * (-1.0 - x_fora) + y_fora

                if ponto_fora == "p1":
                    x1, y1 = x_intersecao, y_intersecao
                else:
                    x2, y2 = x_intersecao, y_intersecao

    def clip_linha_liang_barsky(self, ponto1, ponto2):
        x1, y1 = ponto1
        x2, y2 = ponto2
        delta_x = x2 - x1
        delta_y = y2 - y1
        p = [-delta_x, delta_x, -delta_y, delta_y]
        q = [x1+1, 1-x1, y1+1, 1-y1]
        t1, t2 = 0.0, 1.0

        for k in range(4):
            if p[k] == 0:
                if q[k] < 0: return []            
            else:
                r = q[k] / p[k]                
                if p[k] < 0: t1 = max(t1, r)
                elif p[k] > 0: t2 = min(t2, r)
        if t1 > t2: return []
        return [((x1 + t1 * delta_x), (y1 + t1 * delta_y)), ((x1 + t2 * delta_x), (y1 + t2 * delta_y))]

    def clip_poligono_sutherland_hodgeman(self, pontos_poligono):
        if not pontos_poligono or len(pontos_poligono) < 3: return []
        poligono_atual = pontos_poligono

        for qual_borda in range(4):
            poligono_recortado = []
            tamanho = len(poligono_atual)
            if tamanho == 0: break
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
            y = y1 + dy * (-1.0 - x1) / dx if dx != 0 else y1
        elif qual_borda == 2: 
            x = 1.0
            y = y1 + dy * (1.0 - x1) / dx if dx != 0 else y1
        elif qual_borda == 1: 
            y = -1.0
            x = x1 + dx * (-1.0 - y1) / dy if dy != 0 else x1
        elif qual_borda == 0: 
            y = 1.0
            x = x1 + dx * (1.0 - y1) / dy if dy != 0 else x1
        return (x, y)