class DescritorOBJ:
    def __init__(self, arquivo=None):
        self.arquivo = arquivo
        self.contador_vertices = 1 
        self.cores_usadas = set() 
        self.mtllib_escrever_cabecalho = False

    def escrever_arquivo(self, forma):
        if (self.mtllib_escrever_cabecalho == False):
            self.arquivo.write("mtllib cores.mtl\n")
            self.mtllib_escrever_cabecalho = True

        self.arquivo.write("o {}\n".format(forma.nome))

        cor_usada = forma.cor
        self.cores_usadas.add(cor_usada) 
        nome_cor = "cor_" + cor_usada.lstrip("#")
        self.arquivo.write("usemtl {}\n".format(nome_cor))

        self.arquivo.write("# tipo {}\n".format(forma.tipo))
        
        for ponto in forma.pontos:
            x, y = ponto[0], ponto[1]
            self.arquivo.write("v {} {} 0.0\n".format(x, y))
        
        qtd = len(forma.pontos)    
    
        if qtd == 1:
            self.arquivo.write("p {}\n".format(self.contador_vertices))            
        elif qtd == 2:
            self.arquivo.write("l {} {}\n".format(self.contador_vertices, self.contador_vertices + 1))            
        elif qtd > 2:
            indices = [str(self.contador_vertices + i) for i in range(qtd)]
            if forma.tipo == "wireframe":
                indices.append(str(self.contador_vertices)) 
                self.arquivo.write("l {}\n".format(" ".join(indices)))
            else:
                self.arquivo.write("f {}\n".format(" ".join(indices)))

        self.contador_vertices += qtd 
        
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

    def ler_arquivo(self, caminho_arquivo):
        formas_lidas = []        
        try:
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
                        if len(partes) > 1:
                            cor_objeto = "#" + partes[1].replace("cor_", "")                                        
                    elif linha.startswith("# tipo"):
                        partes = linha.split()
                        if len(partes) > 2:
                            tipo_objeto = partes[2] 
                    elif linha.startswith("v "):
                        partes = linha.split()
                        x = float(partes[1])
                        y = float(partes[2])
                        pontos.append((x, y))             
                    elif linha.startswith("l ") or linha.startswith("p ") or linha.startswith("mtllib") or linha == "" or linha.startswith("#") or linha.startswith("f "):
                        pass
                    else:
                        print("ERRO!", linha)
                        
                if pontos:
                    formas_lidas.append([nome_objeto, tipo_objeto, pontos, cor_objeto])    
                    
        except FileNotFoundError:
            pass 
            
        return formas_lidas