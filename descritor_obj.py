# =====================
# CLASSE DESCRITOR OBJ
# ======================

class DescritorOBJ:
    def __init__(self, arquivo=None):
        self.arquivo = arquivo
        self.contador_vertices = 1 
        self.cores_usadas = set() 
        self.mtllib_escrever_cabecalho = False

    def escrever_arquivo(self, forma):
        if forma.tipo == "CAMERA": return

        if not self.mtllib_escrever_cabecalho:
            self.arquivo.write("mtllib cores.mtl\n")
            self.mtllib_escrever_cabecalho = True

        self.arquivo.write("o {}\n".format(forma.nome))
        cor_usada = forma.cor
        self.cores_usadas.add(cor_usada) 
        nome_cor = "cor_" + cor_usada.lstrip("#")
        self.arquivo.write("usemtl {}\n".format(nome_cor))
        self.arquivo.write("# tipo {}\n".format(forma.tipo))
        
        for ponto in forma.pontos:
            z = ponto[2] if len(ponto) > 2 else 0.0
            self.arquivo.write("v {} {} {}\n".format(ponto[0], ponto[1], z))
            
        for conexao in forma.conexoes:
            indices_globais = [str(i + self.contador_vertices) for i in conexao]
            self.arquivo.write("f {}\n".format(" ".join(indices_globais)))

        self.contador_vertices += len(forma.pontos)
        self.gerar_arquivo_mtl()

    def gerar_arquivo_mtl(self, caminho_mtl="cores.mtl"):
        with open(caminho_mtl, "w", encoding="utf-8") as arquivo_mtl:
            for cor_hex in self.cores_usadas:
                hex_str = cor_hex.lstrip("#")
                nome_mat = "cor_" + hex_str
                r, g, b = int(hex_str[0:2], 16)/255.0, int(hex_str[2:4], 16)/255.0, int(hex_str[4:6], 16)/255.0
                arquivo_mtl.write("newmtl {}\nKd {:.3f} {:.3f} {:.3f}\n\n".format(nome_mat, r, g, b))

    def ler_arquivo(self, caminho_arquivo):
        formas_lidas = []
        offset_global = 0
        try:
            with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
                nome_objeto = "forma"
                cor_objeto = "#000000"
                tipo_objeto = "wireframe"
                pontos = []
                conexoes = []
                
                for linha in arquivo:
                    linha = linha.strip()                
                    if linha.startswith("o "):
                        if pontos:
                            formas_lidas.append([nome_objeto, tipo_objeto, pontos, conexoes, cor_objeto])
                            offset_global += len(pontos)
                            pontos = []; conexoes = []
                        nome_objeto = linha.split(" ", 1)[1]                    
                    elif linha.startswith("usemtl"):
                        partes = linha.split()
                        if len(partes) > 1: cor_objeto = "#" + partes[1].replace("cor_", "")                                        
                    elif linha.startswith("# tipo"):
                        partes = linha.split()
                        if len(partes) > 2: tipo_objeto = partes[2] 
                    elif linha.startswith("v "):
                        partes = linha.split()
                        x, y = float(partes[1]), float(partes[2])
                        z = float(partes[3]) if len(partes) > 3 else 0.0
                        pontos.append((x, y, z))             
                    elif linha.startswith("l ") or linha.startswith("f "):
                        indices = []
                        for v in linha.split()[1:]:
                            idx = int(v.split('/')[0]) - 1 - offset_global
                            indices.append(idx)
                        conexoes.append(indices)

                if pontos:
                    formas_lidas.append([nome_objeto, tipo_objeto, pontos, conexoes, cor_objeto])    
        except FileNotFoundError:
            pass 
        return formas_lidas