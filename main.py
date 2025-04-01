from grafo import Grafo
from algoritmos import *

if __name__ == "__main__":
    # Cria um grafo
    grafo = Grafo()

    # Adiciona vértices e arestas
    grafo.adicionar_aresta('A', 'B')
    grafo.adicionar_aresta('B', 'C')
    grafo.adicionar_aresta('C', 'D')
    grafo.adicionar_aresta('D', 'E')
    grafo.adicionar_aresta('E', 'F')
    grafo.adicionar_aresta('F', 'Z')
    grafo.adicionar_aresta('A', 'X')
    grafo.adicionar_aresta('X', 'Y')
    grafo.adicionar_aresta('Y', 'Z')

    print("Grafo inicial:")
    print(grafo)

    # Gerar matriz de adjacência
    print("Matriz de adjacência:")
    print(grafo.gerar_matriz_adjacencia())

    # Rotas Possíveis
    print("Todas as rotas possíveis para ir do vértice A até o Z: ", encontrar_rotas_possiveis('A', 'Z', grafo.adjacencia))

    # Menor rota
    print("Menor rota para ir do vértice A até o Z: ", encontrar_menor_rota('A', 'Z', grafo.adjacencia))

    # Maior rota
    print("Menor rota para ir do vértice A até o Z: ", encontrar_maior_rota('A', 'Z', grafo.adjacencia))
    
    # Remove uma aresta
    grafo.remover_aresta('A', 'B')
    print("\nGrafo após remover aresta A-B:")
    print(grafo)
    
    # Remove um vértice
    grafo.remover_vertice('C')
    print("\nGrafo após remover vértice C:")
    print(grafo)
