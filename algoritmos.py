def encontrar_rotas_possiveis(inicio, fim, grafo, caminho=[]):
    caminho = caminho + [inicio]
    if inicio == fim:
        return [caminho] 
    # Se o inicio e o fim forem iguais retorna a lista com um único vértice mesmo, isso é considerado um caminho válido.

    if inicio not in grafo:
        return []
    # Ou o vértice não existe, ou não se conecta em nenhum outro

    caminhos_possiveis = []
    # Caso os dois if's acima sejam false, inicializa a lista de caminhos vazia

    for vertice in grafo[inicio]: # Itera em todos vizinhos do vértice inicial
        if vertice not in caminho: # Pra cada vértice adjacente, checa se já não tá no caminho, para evitar ciclos (então nenhum vértice repete na rota).
            # Pra cada vértice que ainda não está no caminho a função se chama recursivamente, passando o vértice atual como inicio, assim continuando a busca até encontrar o vértice alvo
            novos_caminhos = encontrar_rotas_possiveis(vertice, fim, grafo, caminho)
            for novo_caminho in novos_caminhos:
                # Caminhos encontrados são acumulados na lista de caminhos possíveis
                caminhos_possiveis.append(novo_caminho)
    # retorna todos caminhos encontrados
    return caminhos_possiveis

def encontrar_menor_rota(inicio, fim, grafo, caminho=[]):
    caminho = caminho + [inicio]
    if inicio == fim:
        return caminho
    if inicio not in grafo:
        return []
    menor_caminho = None # Inicializa como None pra sinalizar que ainda não existe
    for vertice in grafo[inicio]:
        if vertice not in caminho:
            novo_caminho = encontrar_menor_rota(vertice, fim, grafo, caminho)
            # Daqui pra cima eh igual a função de cima
            if novo_caminho: # Verifica se há um novo caminho 
                # Se não houver um novo caminho ou o novo caminho for menor que o anterior, define o novo caminho como sendo o menor
                if not menor_caminho or len(novo_caminho) < len(menor_caminho):
                    menor_caminho = novo_caminho
    return menor_caminho
    # Obs.: diferente da função de rotas possíveis, essa só guarda um único caminho ao invés de acumular vários.


def encontrar_maior_rota(inicio, fim, grafo, caminho=[]):
    caminho = caminho + [inicio]
    if inicio == fim:
        return caminho
    if inicio not in grafo:
        return []
    maior_caminho = None
    for vertice in grafo[inicio]:
        if vertice not in caminho:
            novo_caminho = encontrar_menor_rota(vertice, fim, grafo, caminho)
            if novo_caminho: 
                if not maior_caminho or len(novo_caminho) > len(maior_caminho): # Essa função toda eh a mesma que a de menor rota, só muda o "<" pra ">" nessa linha
                    maior_caminho = novo_caminho
    return maior_caminho
    