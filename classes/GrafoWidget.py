from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QMenu
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtCore import QRectF, QTimer, Qt
import random

from .utilitarios import interpolar_cor, encontrar_rotas_possiveis, encontrar_menor_rota, encontrar_maior_rota
from classes import GrafoVertices
from classes import GrafoArestas

'''
CLASSE DE WIDGETS

Essa classe herda de QGraphicsView e integra a cena (QGraphicsScene) onde os vértices e as arestas são adicionados. Ela gerencia:
- Criação dos vértices e arestas com funções.
- Física (to-do).
- Eventos do mouse para permitir seleção e movimento dos vértices.
- Atualização da cena, garantido que os vértices e arestas sejam reposicionados e atualizados em uma taxa constante de tempo.
'''
class GrafoWidget(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing) # Suavização de cantos

        self.vertices = {} # Dicionário que vai armazenar os vértices. Ex: {vertice_id : GrafoVertice}.
        self.arestas = [] # Lista de arestas.

        self.proximo_vertice_id = 1
        self.vertice_selecionado = None

        self.comeco_aresta = None
        self.vertice_hover = None

        self.fade_alpha = 0.15
        self.fps_delay = 10 # 10ms =~ 100FPS.

        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar_grafo) # Atualiza o grafo quando o timer toca (a cada 10ms)
        self.timer.start(self.fps_delay) # Inicia o timer com 10ms, resetando toda a vez que acaba
        self.setMouseTracking(True)

        # Cores padrão (Vértice normal, selecionado e outros que não estão conectados ao selecionado).
        self.cor_padrao = QColor(170, 170, 170)
        self.cor_selecionado = QColor(138, 92, 236)
        self.cor_dessaturado = QColor(28, 28, 28)

        # Desabilitar o scroll da janela.
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        # Tamanho da tela dos grafos.
        self.setSceneRect(QRectF(0, 0, 640, 360))

    def adicionar_vertice(self, x = 320, y = 180):
        vertice = GrafoVertices(self.proximo_vertice_id, x, y, cor=self.cor_padrao)

        print(f'Vértice {self.proximo_vertice_id} criado em ({x}, {y})')  # Debug

        self.proximo_vertice_id += 1
        self.scene.addItem(vertice)
        self.vertices[vertice.vertice_id] = vertice
        return vertice

    def adicionar_aresta(self, vertice1, vertice2):
        if vertice1 and vertice2 and vertice1 != vertice2:
            aresta = GrafoArestas(vertice1, vertice2, cor=self.cor_padrao)

            print(f'Aresta criada entre {vertice1.vertice_id} e {vertice2.vertice_id}')  # Debug

            self.scene.addItem(aresta)
            self.arestas.append(aresta)

    def resetar_grafo(self):
        for vertice in list(self.vertices.values()):
            self.scene.removeItem(vertice) # Remove cada vértice da tela.
        for aresta in self.arestas:
            self.scene.removeItem(aresta) # Remove cada aresta da tela.
        self.vertices.clear() # Apaga todos os valores do dicionário de vértices.
        self.arestas.clear() # Apaga todos os valores da lista de arestas.
        self.proximo_vertice_id = 1 # Reseta o índice atual dos vértices.

    def atualizar_grafo(self):
        # self.aplicar_fisica() # Inicia a física do grafo (to-do)
        self.atualizar_cores()

        for aresta in self.arestas:
            aresta.atualizar_posicao()

        self.scene.update() # Força a cena a atualizar (Evita nós cortados quando se mexem muito rápido)

    def aplicar_fisica(self):
        pass

    def atualizar_cores(self):
        # Atualiza as cores dos vértices
        for vertice in self.vertices.values():
            alvo = self.cor_padrao
            if self.vertice_hover is not None: # Verifica se o vértice com o cursor por cima está conectado com os outros
                if (vertice == self.vertice_hover or
                        self.esta_diretamente_conectado(self.vertice_hover, vertice)):
                    alvo = self.cor_selecionado
                else:
                    alvo = self.cor_dessaturado
            vertice.cor_atual = interpolar_cor(vertice.cor_atual, alvo, self.fade_alpha) # Mudar cor de forma suave

            vertice.update()

        # Atualiza as cores das arestas
        for aresta in self.arestas:
            alvo = self.cor_padrao
            if self.vertice_hover is not None: # Verifica apenas conexão direta com o vértice "hover" (com o cursor em cima)
                if (aresta.vertice1 == self.vertice_hover or
                        aresta.vertice2 == self.vertice_hover):
                    alvo = self.cor_selecionado
                else:
                    alvo = self.cor_dessaturado

            aresta.cor_atual = interpolar_cor(aresta.cor_atual, alvo, self.fade_alpha)
            aresta.atualizar_cor()

            # Atualizar cores das arestas
            for aresta in self.arestas:
                alvo = self.cor_padrao
                if self.vertice_hover is not None:
                    if aresta.vertice1.vertice_id == self.vertice_hover.vertice_id or aresta.vertice2.vertice_id == self.vertice_hover.vertice_id or self.esta_diretamente_conectado(self.vertice_hover, aresta.vertice1) or self.esta_diretamente_conectado(self.vertice_hover, aresta.vertice2):
                        alvo = self.cor_selecionado
                    else:
                        alvo = self.cor_dessaturado

                aresta.cor_atual = interpolar_cor(aresta.cor_atual, alvo, self.fade_alpha)
                aresta.atualizar_cor()

    def esta_diretamente_conectado(self, vertice_a: GrafoVertices, vertice_b: GrafoVertices) -> bool:
        for aresta in self.arestas:
            if (aresta.vertice1 == vertice_a and aresta.vertice2 ==  vertice_b) or (aresta.vertice1 == vertice_b and aresta.vertice2 ==  vertice_a):
                return True
        return False # Retorna falso apenas se nenhuma aresta conectar os vértices.

    # Eventos do mouse para selecionar a mover vértices
    def mousePressEvent(self, event):
        pos = self.mapToScene(event.pos())
        itens = self.scene.items(pos)

        # Se o clique for do botão direito fora de um vertice, nao faz nada, só chama o menu de contexto padrao
        # Se o clique for em um vertice chama o menu de contexto para vertices
        if event.button() == Qt.MouseButton.RightButton:
            for item in itens:
                if isinstance(item, GrafoVertices):
                    self.menu_contexto_vertice(item, event.globalPosition().toPoint())
                    return
            self.menu_contexto_padrao(event.globalPosition().toPoint())
            return


        for item in itens:
            if isinstance(item, GrafoVertices):
                item.fixo = True
                self.vertice_selecionado = item
                print(f"Vértice selecionado: {item.vertice_id}")  # Debug
                if self.comeco_aresta is not None:
                    self.adicionar_aresta(self.comeco_aresta, item)
                    self.comeco_aresta = None
                return

        novo_vertice = self.adicionar_vertice(pos.x(), pos.y())
        self.vertice_selecionado = novo_vertice

        print(f"Novo vértice criado: {novo_vertice.vertice_id}")  # Debug

        super().mousePressEvent(event)
    
    def menu_contexto_vertice(self, vertice, pos):
        """Exibe o menu de contexto para vertices."""
        menu_contexto_vertice = QMenu()
        acao_remover = menu_contexto_vertice.addAction("Remover nó")
        acao_fixar = menu_contexto_vertice.addAction("Fixar nó")
        acao_desconectar = menu_contexto_vertice.addAction("Desconectar nó")

        acao_remover.triggered.connect(lambda: print("Ainda não implementado"))
        acao_fixar.triggered.connect(lambda: print("Ainda não implementado"))
        acao_desconectar.triggered.connect(lambda: print("Ainda não implementado"))

        menu_contexto_vertice.exec(pos)

    def menu_contexto_padrao(self, pos):
        """Exibe o menu de contexto padrão."""
        menu = QMenu()
        acao_inserir = menu.addAction("Inserir nó")
        acao_resetar = menu.addAction("Limpar grafo")
        acao_gerar = menu.addAction("Gerar novo grafo")

        # Conecta as ações
        acao_inserir.triggered.connect(lambda: self.adicionar_vertice())
        acao_resetar.triggered.connect(self.resetar_grafo)
        acao_gerar.triggered.connect(self.gerar_grafo)

        menu.exec(pos)

    def mouseMoveEvent(self, event):
        pos = self.mapToScene(event.pos())
        if self.vertice_selecionado and self.vertice_selecionado.fixo:
            self.vertice_selecionado.setPos(pos)
        itens = self.scene.items(pos)
        self.vertice_hover = None

        for item in itens:
            if isinstance(item, GrafoVertices):
                self.vertice_hover = item
                break

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if self.vertice_selecionado:
            self.vertice_selecionado.fixo = False

        super().mouseReleaseEvent(event)
    
    def gerar_grafo(self):
        if self.proximo_vertice_id == 1:
            for i in range(6):
                x = random.randint(0, 640)
                y = random.randint(0, 360)
                self.adicionar_vertice(x, y)

            vertices = list(self.vertices.values())
            conexoes = random.randint(6, 10)

            for _ in range(conexoes):
                vert1, vert2 = random.sample(vertices, 2) # 2 vértices aleatórios
                self.adicionar_aresta(vert1, vert2)
        else:
            self.resetar_grafo()
            self.gerar_grafo()

    def criar_dicionario_adjacencia(self):
        adjacencia = {}

        for vertice_id in self.vertices.keys():
            adjacencia[vertice_id] = []
        
        for aresta in self.arestas:
            vertice1_id = aresta.vertice1.vertice_id
            vertice2_id = aresta.vertice2.vertice_id

            adjacencia[vertice1_id].append(vertice2_id)
            adjacencia[vertice2_id].append(vertice1_id)
    
        return adjacencia
    
    def desenhar_todas_rotas(self):
        adjacencia = self.criar_dicionario_adjacencia()
        caminhos_possiveis = encontrar_rotas_possiveis(1, 4, adjacencia)
        print(caminhos_possiveis)
        return caminhos_possiveis

    def desenhar_menor_rota(self):
        adjacencia = self.criar_dicionario_adjacencia()
        caminhos_possiveis = encontrar_menor_rota(1, 4, adjacencia)
        print(caminhos_possiveis)
        return caminhos_possiveis
    
    def desenhar_maior_rota(self):

        adjacencia = self.criar_dicionario_adjacencia()
        caminhos_possiveis = encontrar_maior_rota(1, 4, adjacencia)
        print(caminhos_possiveis)
        return caminhos_possiveis
    
    