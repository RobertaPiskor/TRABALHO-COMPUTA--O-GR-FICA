import os

# =====================
# CLASSE DESCRITOR OBJ
# ======================

class DescritorOBJ:
    def __init__(self, arquivo=None, nome_mtl="cores.mtl"):
        self.arquivo = arquivo
        self.contador_vertices = 1 
        self.cores_usadas = set() 
        self.mtllib_escrever_cabecalho = False
        self.nome_mtl = nome_mtl

    def escrever_arquivo(self, forma):
        if getattr(forma, 'tipo', '') == "CAMERA" or getattr(forma, 'tipo', '') == "curva": 
            return

        if not self.mtllib_escrever_cabecalho:
            self.arquivo.write(f"mtllib {self.nome_mtl}\n")
            self.mtllib_escrever_cabecalho = True

        self.arquivo.write("o {}\n".format(forma.nome))
        cor_usada = forma.cor
        self.cores_usadas.add(cor_usada) 
        
        nome_mat = "mat_" + cor_usada.lstrip("#")
        self.arquivo.write("usemtl {}\n".format(nome_mat))
        self.arquivo.write("# tipo {}\n".format(forma.tipo))
        
        for ponto in forma.pontos:
            z = ponto[2] if len(ponto) > 2 else 0.0
            self.arquivo.write("v {} {} {}\n".format(ponto[0], ponto[1], z))
            
        for conexao in forma.conexoes:
            indices_globais = [str(i + self.contador_vertices) for i in conexao]
            if len(conexao) == 1:
                self.arquivo.write("p {}\n".format(" ".join(indices_globais)))
            elif len(conexao) == 2:
                self.arquivo.write("l {}\n".format(" ".join(indices_globais)))
            else:
                self.arquivo.write("f {}\n".format(" ".join(indices_globais)))

        self.contador_vertices += len(forma.pontos)

    def gerar_arquivo_mtl(self, caminho_mtl):
        with open(caminho_mtl, "w", encoding="utf-8") as arquivo_mtl:
            for cor_hex in self.cores_usadas:
                hex_str = cor_hex.lstrip("#")
                nome_mat = "mat_" + hex_str
                # Converte Hex para RGB entre 0 e 1 (Kd)
                r, g, b = int(hex_str[0:2], 16)/255.0, int(hex_str[2:4], 16)/255.0, int(hex_str[4:6], 16)/255.0
                arquivo_mtl.write("newmtl {}\nKd {:.3f} {:.3f} {:.3f}\n\n".format(nome_mat, r, g, b))

    def extrair_cor_mtl(self, caminho_mtl, nome_material):
        try:
            with open(caminho_mtl, "r", encoding="utf-8") as mtl:
                lendo_alvo = False
                for linha in mtl:
                    linha = linha.strip()
                    if linha.startswith("newmtl "):
                        mat_name = linha.split(" ", 1)[1]
                        lendo_alvo = (mat_name == nome_material)
                    elif lendo_alvo and linha.startswith("Kd "):
                        partes = linha.split()
                        r, g, b = float(partes[1]), float(partes[2]), float(partes[3])
                        # Converte de volta para Hexadecimal garantindo os limites
                        r_hex = max(0, min(255, int(r * 255)))
                        g_hex = max(0, min(255, int(g * 255)))
                        b_hex = max(0, min(255, int(b * 255)))
                        return f"#{r_hex:02x}{g_hex:02x}{b_hex:02x}"
        except FileNotFoundError:
            pass
        return "#000000" 

    def ler_arquivo(self, caminho_arquivo):
        caminho_absoluto = os.path.abspath(caminho_arquivo)
        dir_atual = os.path.dirname(caminho_absoluto)
        formas_lidas = []
        offset_global = 0
        
        try:
            with open(caminho_absoluto, "r", encoding="utf-8") as arquivo:
                nome_objeto = "forma"
                cor_objeto = "#000000"
                tipo_objeto = "wireframe"
                pontos = []
                conexoes = []
                arquivo_mtl_atual = "cores.mtl"
                
                for linha in arquivo:
                    linha = linha.strip()                
                    if linha.startswith("o "):
                        if pontos:
                            formas_lidas.append([nome_objeto, tipo_objeto, pontos, conexoes, cor_objeto])
                            offset_global += len(pontos)
                            pontos = []; conexoes = []
                        nome_objeto = linha.split(" ", 1)[1]
                        cor_objeto = "#000000"
                        tipo_objeto = "wireframe"
                        
                    elif linha.startswith("mtllib "):
                        arquivo_mtl_atual = linha.split(" ", 1)[1]
                        
                    elif linha.startswith("usemtl"):
                        partes = linha.split()
                        if len(partes) > 1:
                            nome_material = partes[1]
                            caminho_mtl = os.path.join(dir_atual, arquivo_mtl_atual)
                            cor_objeto = self.extrair_cor_mtl(caminho_mtl, nome_material)
                                                
                    elif linha.startswith("# tipo"):
                        partes = linha.split()
                        if len(partes) > 2: tipo_objeto = partes[2] 
                        
                    elif linha.startswith("v "):
                        partes = linha.split()
                        x, y = float(partes[1]), float(partes[2])
                        z = float(partes[3]) if len(partes) > 3 else 0.0
                        pontos.append((x, y, z))             
                    
                    elif linha.startswith("l ") or linha.startswith("f ") or linha.startswith("p "):
                        indices = []
                        for v in linha.split()[1:]:
                            idx = int(v.split('/')[0]) - 1 - offset_global
                            indices.append(idx)
                        conexoes.append(indices)

                if pontos:
                    formas_lidas.append([nome_objeto, tipo_objeto, pontos, conexoes, cor_objeto])    
                    
        except FileNotFoundError:
            print(f"AVISO: Arquivo não encontrado - {caminho_absoluto}")
            pass 
            
        return formas_lidas