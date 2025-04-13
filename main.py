import sys, math
import random

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QToolBar,
    QVBoxLayout, QGraphicsItem, QGraphicsEllipseItem, QGraphicsTextItem,
    QGraphicsLineItem
)
from PyQt6.QtGui import QBrush, QPen, QColor, QPainter, QAction, QMouseEvent, QIcon
from PyQt6.QtCore import QRectF, QTimer, Qt, QPointF

def interpolar_cor(c1: QColor, c2: QColor, alpha: float) -> QColor:
    r = int(c1.red() + alpha * (c2.red() - c1.red()))
    g = int(c1.green() + alpha * (c2.green() - c1.green()))
    b = int(c1.blue() + alpha * (c2.blue() - c1.blue()))
    return QColor(r, g, b)

def encontrar_rotas_possiveis(inicio, fim, grafo, caminho=[]):
    caminho = caminho + [inicio]
    if inicio == fim:
        return [caminho]
    # Se o início e o fim forem iguais retorna a lista com um único vértice mesmo, isso é considerado um caminho válido.

    if inicio not in grafo:
        return []
    # Ou o vértice não existe, ou não se conecta em nenhum outro

    caminhos_possiveis = []
    # Caso os dois if's acima sejam false, inicializa a lista de caminhos vazia

    for vertice in grafo[inicio]: # Itera em todos os vizinhos do vértice inicial
        if vertice not in caminho: # Para cada vértice adjacente, checa se já não tá no caminho, para evitar ciclos (então nenhum vértice repete na rota).
            # Para cada vértice que ainda não está no caminho a função se chama recursivamente, passando o vértice atual como inicio, assim continuando a busca até encontrar o vértice alvo
            novos_caminhos = encontrar_rotas_possiveis(vertice, fim, grafo, caminho)
            for novo_caminho in novos_caminhos:
                # Caminhos encontrados são acumulados na lista de caminhos possíveis
                caminhos_possiveis.append(novo_caminho)
    # retorna todos os caminhos encontrados
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
            # Daqui para cima é igual à função de cima
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

'''
CLASSE DE VÉRTICES

Essa classe herda de 'QGraphicsEllipseItem', um componente que desenha círculos
com propriedades que podem ser modificadas de qualquer forma. Cada vértice tem as 
seguintes propriedades:
- Um ID.
- raio.
- Posição atual.
- Cor da borda e fundo.
- Um 'QGraphicsTextItem' filho, que exibe seu ID no centro do vértice.
'''
class GrafoVertices(QGraphicsEllipseItem):
    def __init__(self, vertice_id, x, y, raio = 20, cor = QColor(128, 128, 128)):
        super().__init__(-raio, -raio, 2*raio, 2*raio) # (posição x, posição y, largura, altura)

        self.vertice_id = vertice_id
        self.setPos(x, y)
        self.raio = raio

        self.cor_atual = cor
        self.cor_alvo = cor

        self.update()

        # Variáveis pra usar na física
        self.vx = 0.0
        self.vy = 0.0

        self.fixo = False

        self.setFlags(
            QGraphicsItem.GraphicsItemFlag.ItemIsSelectable |
            QGraphicsItem.GraphicsItemFlag.ItemIsMovable
        ) # Flags que permitem que os vértices sejam selecionados e movidos.
        self.setAcceptHoverEvents(True)

        # Texto no centro do vértice
        self.texto = QGraphicsTextItem(str(vertice_id), self)
        self.texto.setDefaultTextColor(Qt.GlobalColor.white)
        limite = self.texto.boundingRect()
        self.texto.setPos(-limite.width()/2, -limite.height()/2)

    def paint(self, painter: QPainter, opcao, widget = None):
        painter.setRenderHint(QPainter.RenderHint.Antialiasing) # Ativar suavização dos cantos dos objetos.

        # Cor dos cantos do vértice.
        pen = QPen(Qt.GlobalColor.black)
        painter.setPen(pen)

        # Cor de fundo do vértice.
        brush = QBrush(self.cor_atual)
        painter.setBrush(brush)

        # Desenhar o vértice.
        painter.drawEllipse(self.rect())

'''
CLASSE DE ARESTAS

Essa classe herda de 'QGraphicsLineItem', um componente que desenha linhas e suas propriedades:
- Vértices que ela está ligando
- Cor atual
- Cor alvo
'''
class GrafoArestas(QGraphicsLineItem):
    def __init__(self, vertice1: GrafoVertices, vertice2: GrafoVertices, cor = QColor(128, 128, 128)):
        super().__init__()

        self.vertice1 = vertice1
        self.vertice2 = vertice2

        self.cor_atual = cor
        self.cor_alvo = cor

        pen = QPen(self.cor_atual)
        pen.setWidth(2)

        self.setPen(pen)
        self.setZValue(-1) # Garante que as arestas fiquem por trás dos vértices

        self.atualizar_posicao()

    # Função que ajusta as arestas conforme os vértices se movem
    def atualizar_posicao(self):
        p1 = self.vertice1.pos()
        p2 = self.vertice2.pos()

        self.setLine(p1.x(), p1.y(), p2.x(), p2.y())

    def atualizar_cor(self):
        pen = self.pen()
        pen.setColor(self.cor_atual)
        self.setPen(pen)

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
        self.cor_dessaturado = QColor(60, 60, 60)

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
        if vertice1 == vertice2:
            print('Sem criação de laços!')
            return

        # Verificar se a aresta já existe
        for aresta in self.arestas:
            if ((aresta.vertice1 == vertice1 and aresta.vertice2 == vertice2) or
                (aresta.vertice1 == vertice2 and aresta.vertice2 == vertice1)):
                print(f'Conexão já existe entre {vertice1.vertice_id} e {vertice2.vertice_id}!')
                return

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

    def gerar_grafo(self):
        if self.proximo_vertice_id == 1:
            for i in range(12):
                x = random.randint(0, 640)
                y = random.randint(0, 360)
                self.adicionar_vertice(x, y)

            vertices = list(self.vertices.values())
            conexoes = random.randint(6, 15)

            for _ in range(conexoes):
                vert1, vert2 = random.sample(vertices, 2) # Escolhe 2 vértices aleatórios
                self.adicionar_aresta(vert1, vert2)
        else:
            self.resetar_grafo()
            self.gerar_grafo()

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

    def esta_diretamente_conectado(self, vertice_a: GrafoVertices, vertice_b: GrafoVertices) -> bool:
        for aresta in self.arestas:
            if (aresta.vertice1 == vertice_a and aresta.vertice2 == vertice_b) or (aresta.vertice1 == vertice_b and aresta.vertice2 == vertice_a):
                return True
        return False # Retorna falso apenas se nenhuma aresta conectar os vértices.

    # Eventos do mouse para selecionar a mover vértices
    def mousePressEvent(self, event):
        pos = self.mapToScene(event.pos())
        itens = self.scene.items(pos)

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

'''
CLASSE DA JANELA PRINCIPAL

Essa classe herda do componente 'QMainWindow' e integra a classe GrafoWidget como seu conteúdo principal. Além disso, ela cria uma barra de ferramentas para ações globais, como:
- Adicionar vértices.
- Adicionar arestas.
- Resetar o grafo.
'''
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Grafla') # Nome da janela
        self.setWindowIcon(QIcon('GraflaIcone.ico'))

        self.grafoWidget = GrafoWidget()
        self.setCentralWidget(self.grafoWidget)

        toolbar = QToolBar('Barra de Ferramentas')
        self.addToolBar(toolbar)

        botao_adicionar_vertice = QAction('Adicionar vertice', self)
        botao_adicionar_vertice.triggered.connect(lambda: self.grafoWidget.adicionar_vertice())
        toolbar.addAction(botao_adicionar_vertice)

        botao_adicionar_aresta = QAction('Adicionar aresta', self)
        botao_adicionar_aresta.triggered.connect(self.comecar_aresta)
        toolbar.addAction(botao_adicionar_aresta)

        botao_resetar = QAction('Resetar', self)
        botao_resetar.triggered.connect(lambda: self.grafoWidget.resetar_grafo())
        toolbar.addAction(botao_resetar)

        botao_gerar_grafo = QAction('Novo Grafo', self)
        botao_gerar_grafo.triggered.connect(lambda: self.grafoWidget.gerar_grafo())
        toolbar.addAction(botao_gerar_grafo)

        botao_encontrar_todas_rotas = QAction('Encontrar rotas possíveis', self)
        botao_encontrar_todas_rotas.triggered.connect(lambda: self.grafoWidget.desenhar_todas_rotas())
        toolbar.addAction(botao_encontrar_todas_rotas)

    def comecar_aresta(self):
        if self.grafoWidget.vertice_selecionado:
            self.grafoWidget.comeco_aresta = self.grafoWidget.vertice_selecionado

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1280, 720)  # Tamanho inicial da janela (Pode ser modificado pelo usuário)
    window.show()
    sys.exit(app.exec())