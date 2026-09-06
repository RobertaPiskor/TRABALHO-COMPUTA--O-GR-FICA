# ========================
# CLASSE DESCRITOR OBJETO
# ========================

class DescritorOBJ:
    
    def __init__(self, arquivo=None):
        self.arquivo = arquivo
        self.contador_vertices = 1 

    # ==========================================
    #  Escrever no arquivo

    def escrever_arquivo(self, forma):
        self.arquivo.write(f"o {forma.nome}\n")
        cor = getattr(forma, 'cor', "#000000") # Para não dar erro na questão da cor
        if cor is None or cor == "None" or cor == "":
            cor = "#000000" 
        self.arquivo.write(f"# cor {cor}\n")
        for ponto in forma.pontos:
            if isinstance(ponto, (tuple, list)):
                x, y = ponto[0], ponto[1]
            else:
                x, y = ponto.x, ponto.y
            self.arquivo.write(f"v {x} {y} 0.0\n")
        num_pontos = len(forma.pontos)
        if num_pontos > 1:
            for i in range(num_pontos):
                p1 = self.contador_vertices + i
                p2 = self.contador_vertices + ((i + 1) % num_pontos) 
                self.arquivo.write(f"l {p1} {p2}\n")
        self.contador_vertices += num_pontos

    # =====================================
    # Para ver o que tem dentro do arquivo

    def ler_arquivo(self, caminho_arquivo):
        formas_lidas = []        
        with open(caminho_arquivo, "r", encoding="utf-8") as arquivo:
            nome_objeto = "Objeto_Desconhecido"
            cor_objeto = "#000000"
            pontos = []
            for linha in arquivo:
                linha = linha.strip()                
                if linha.startswith("o "):
                    if pontos:
                        formas_lidas.append({"nome": nome_objeto, "cor": cor_objeto, "pontos": pontos})
                        pontos = [] 
                    nome_objeto = linha.split(" ", 1)[1]                    
                elif linha.startswith("# cor"):
                    partes = linha.split()
                    if len(partes) > 2:
                        cor_objeto = partes[2]
                        if cor_objeto == "None":
                            cor_objeto = "#000000"                            
                elif linha.startswith("v "):
                    partes = linha.split()
                    if len(partes) >= 3:
                        x = float(partes[1])
                        y = float(partes[2])
                        pontos.append((x, y))                        
            if pontos:
                formas_lidas.append({"nome": nome_objeto, "cor": cor_objeto, "pontos": pontos})    
        return formas_lidas