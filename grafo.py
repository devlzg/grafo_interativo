class Grafo:
    def __init__(self):
        # O grafo será representado por um dicionário, onde cada chave é um vértice,
        # e os valores são listas com os vértices conectados a ele.
        # Também tem uma lista de arestas, que armazena as conexões entre os vértices. [(vértice1, vértice2), ...]
        self.adjacencia = {} # Inicializando dicionário
        self.arestas = []

    def adicionar_vertice(self, vertice):
        # Verifica se o vértice já existe antes de adicionar ele
        if vertice not in self.adjacencia:
            self.adjacencia[vertice] = [] # Inicializa lista de vizinhos do vértice dentro do dicionário
        else:
            print(f"O vértice {vertice} já existe no grafo.")

    def remover_vertice(self, vertice):
        # Remove o vertice e todas as arestas conectadas a ele
        if vertice in self.adjacencia:
            # Pra cada vizinho de um vertice, remove a vizinhança entre eles
            for vizinho in self.adjacencia[vertice]:
                self.adjacencia[vizinho].remove(vertice)
                self.arestas.remove((min(vertice, vizinho), max(vertice, vizinho))) # importante lembrar que é uma tupla
                # Esse min e max são importantes por se tratar de um grafo nao orientado, então o codigo sempre assume que vertice > vizinho, prevenindo erros
            # Retira o vertice do grafo
            del self.adjacencia[vertice]

    def adicionar_aresta(self, vertice1, vertice2):

        # Adiciona os vértices caso não existam
        if vertice1 not in self.adjacencia:
            self.adicionar_vertice(vertice1)
        if vertice2 not in self.adjacencia:
            self.adicionar_vertice(vertice2)

        # Adiciona uma aresta entre dois vértices (não direcionado)
        if vertice1 in self.adjacencia and vertice2 in self.adjacencia:
            self.adjacencia[vertice1].append(vertice2)
            self.adjacencia[vertice2].append(vertice1)
        else:
            print("Um dos vértices não existe.")

        # Armazenando sempre ordenado (alfabética ou numéricamente) pra facilitar na hora de manipular e evitar duplicatas
        aresta = (min(vertice1, vertice2), max(vertice1, vertice2))
        if aresta not in self.arestas:
            self.arestas.append(aresta)
        else:
            print("Essa aresta já existe")
    
    def remover_aresta(self, vertice1, vertice2):
        if vertice1 in self.adjacencia and vertice2 in self.adjacencia[vertice1]:
            self.adjacencia[vertice1].remove(vertice2)
            self.adjacencia[vertice2].remove(vertice1)
        
        aresta = (min(vertice1, vertice2), max(vertice1, vertice2))
        if aresta in self.arestas:
            self.arestas.remove(aresta)
    
    def get_vertices(self):
        # Retorna uma snapshot dos vertices atuais (keys == vertices no dicionario de adjacencia do grafo)
        return list(self.adjacencia.keys())

    def get_arestas(self):
        # Similiar à função get_vertices, é importante que sejam snapshots para que quem for usar essas funções nao altere sem querer a estrutura original
        return list(self.arestas.copy())

    def get_vizinhos(self, vertice):
        # O .get() procura na adjacencia a key (vertice) e retorna seus valores.
        # Caso não encontre o vertice ele retorna o segundo argumento passado, uma lista vazia.
        # O .copy() cria uma snapshot.
        return self.adjacencia.get(vertice, []).copy()

    def __str__(self):
        # Representando o grafo em string
        return f"Vértices: {self.get_vertices()}\nArestas: {self.get_arestas()}"