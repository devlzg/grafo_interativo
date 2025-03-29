from grafo import Grafo

if __name__ == "__main__":
    # Cria um grafo
    grafo = Grafo()

    # Adiciona vértices e arestas
    grafo.adicionar_aresta('A', 'B')
    grafo.adicionar_aresta('A', 'C')
    grafo.adicionar_aresta('B', 'C')
    grafo.adicionar_aresta('C', 'D')
    
    print("Grafo inicial:")
    print(grafo)
    
    # Remove uma aresta
    grafo.remover_aresta('A', 'B')
    print("\nGrafo após remover aresta A-B:")
    print(grafo)
    
    # Remove um vértice
    grafo.remover_vertice('C')
    print("\nGrafo após remover vértice C:")
    print(grafo)