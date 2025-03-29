from grafo import Grafo

if __name__ == "__main__":
    # Cria um grafo
    grafo = Grafo()

    # Adiciona vértices e arestas
    grafo.adicionar_aresta('São Paulo', 'Rio de Janeiro')
    grafo.adicionar_aresta('São Paulo', 'Belo horizonte')
    grafo.adicionar_aresta('Rio de Janeiro', 'Belo horizonte')
    grafo.adicionar_aresta('Belo horizonte', 'Brasília')
    
    print("Grafo inicial:")
    print(grafo)
    
    # Remove uma aresta
    grafo.remover_aresta('São Paulo', 'Rio de Janeiro')
    print("\nGrafo após remover aresta São Paulo-Rio de Janeiro:")
    print(grafo)
    
    # Remove um vértice
    grafo.remover_vertice('Belo horizonte')
    print("\nGrafo após remover vértice Belo horizonte:")
    print(grafo)