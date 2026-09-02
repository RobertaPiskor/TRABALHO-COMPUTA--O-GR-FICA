
import tkinter as tk
from aplicacao_cg import AplicacaoCG
from janela_transformada import JanelaTransformacoes
from formas_geometricas import FormasGeometricas


# 1. Criar a figura com os pontos originais
triangulo = FormasGeometricas.drawWireframe("Triangulo", [(66, 90), (-12, 54), (100, -200)])

# 2. Pegar a Matriz de Translação
matriz_T = FormasGeometricas.get_matriz_translacao(-6, 10)

# 3. Pegar a Matriz de Rotação na Origem (90 graus)
matriz_R = FormasGeometricas.get_matriz_rotacao_origem(90)

# 4. Criar a Matriz de Escalonamento na Origem (2x)
matriz_S = [
    [2, 0, 0],
    [0, 2, 0],
    [0, 0, 1]
]

# 5. Compor as matrizes na ordem correta (T * R * S)
matriz_TR = FormasGeometricas.multiplicacao_matrizes(matriz_T, matriz_R)
matriz_composta = FormasGeometricas.multiplicacao_matrizes(matriz_TR, matriz_S)

# 6. Aplicar no triângulo
triangulo.aplicar_matriz_transformacao(matriz_composta)

# Printar os novos pontos arredondados para conferir
print("Novos pontos:")
for x, y in triangulo.pontos:
    print(f"({round(x)}, {round(y)})")