# ========================
# CLASSE DESCRITOR OBJETO
# ========================

class DescritorOBJ:
    
    def __init__(self, arquivo=None):
        self.arquivo = arquivo
        self.contador_vertices = 1 
        self.cores_usadas = set() 
        self.mtllib_escrito = False

    # =====================
    #  Escrever no arquivo

    def escrever_arquivo(self, forma):
        self.arquivo.write("mtllib cores.mtl\n")
        self.arquivo.write("o {}\n".format(forma.nome))
        cor = getattr(forma, 'cor', "#000000") # Para não dar erro na questão da cor
        if cor is None or cor == "None" or cor == "":
            cor = "#000000"
        self.cores_usadas.add(cor) 
        nome_cor = "cor_" + cor.lstrip("#")
        self.arquivo.write("usemtl {}\n".format(nome_cor))
        self.arquivo.write("# tipo {}\n".format(forma.tipo))
        for ponto in forma.pontos:
            x, y = ponto[0], ponto[1]
            self.arquivo.write("v {} {} 0.0\n".format(x, y))
        if len(forma.pontos) == 1:
            self.arquivo.write("p {}\n".format(self.contador_vertices))
        if len(forma.pontos) > 1: # to considerando que temos que salvar arestas e vertices (o ideal e exemplicificado no manual dizia para fazer "face")
            for i in range(len(forma.pontos) ):
                p1 = self.contador_vertices + i
                p2 = self.contador_vertices + ((i + 1) % len(forma.pontos) ) 
                self.arquivo.write("l {} {}\n".format(p1,p2))
        self.contador_vertices += len(forma.pontos) 
        
        self.gerar_arquivo_mtl()

    def gerar_arquivo_mtl(self, caminho_mtl="cores.mtl"):
        with open(caminho_mtl, "w", encoding="utf-8") as arquivo_mtl:
            for cor_hex in self.cores_usadas:
                hexadecimal_sem_velha = cor_hex.lstrip("#")
                nome_material = "cor_" + hexadecimal_sem_velha

                red_cor = int(hexadecimal_sem_velha[0:2], 16) / 255.0
                green_cor = int(hexadecimal_sem_velha[2:4], 16) / 255.0
                blue_cor = int(hexadecimal_sem_velha[4:6], 16) / 255.0
                
                arquivo_mtl.write("newmtl {}\n".format(nome_material))
                arquivo_mtl.write("Kd {:.3f} {:.3f} {:.3f}\n\n".format(red_cor, green_cor, blue_cor))

    # =====================================
    # Para ver o que tem dentro do arquivo

    def ler_arquivo(self, caminho_arquivo):
        formas_lidas = []        
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            nome_objeto = "forma"
            cor_objeto = "#000000"
            tipo_objeto = "wireframe"
            pontos = []
            
            for linha in arquivo:
                linha = linha.strip()                
                if linha.startswith("o "):
                    if pontos:
                        formas_lidas.append([nome_objeto, tipo_objeto, pontos, cor_objeto])
                        pontos = [] 
                    nome_objeto = linha.split(" ", 1)[1]                    
                elif linha.startswith("usemtl"):
                    partes = linha.split()
                    cor_objeto = "#" + partes[1].replace("cor_", "")                                          
                elif linha.startswith("# tipo"):
                    partes = linha.split()
                    tipo_objeto = partes[2]
                elif linha.startswith("v "):
                    partes = linha.split()
                    x = float(partes[1])
                    y = float(partes[2])
                    pontos.append((x, y))             
                elif linha.startswith("l ") or linha.startswith("p ") or linha.startswith("mtllib") or linha == "" or linha.startswith("#"):
                    pass # FUTURO
                else:
                    print("ERRO!", linha)
                    
            if pontos:
                formas_lidas.append([nome_objeto, tipo_objeto, pontos, cor_objeto])    
                
        return formas_lidas