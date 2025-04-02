import sys, math

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QGraphicsView, QGraphicsScene, QToolBar,
    QVBoxLayout, QGraphicsItem, QGraphicsEllipseItem, QGraphicsTextItem, QGraphicsLineItem
)
from PyQt6.QtGui import QBrush, QPen, QColor, QPainter, QAction, QMouseEvent
from PyQt6.QtCore import QRectF, QTimer, Qt, QPointF

def interpolar_cor(c1: QColor, c2: QColor, alpha: float) -> QColor:
    r = int(c1.red() + alpha * (c2.red() - c1.red()))
    g = int(c1.green() + alpha * (c2.green() - c1.green()))
    b = int(c1.blue() + alpha * (c2.blue() - c1.blue()))
    return QColor(r, g, b)

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
        # Atualiza cores dos nós com interpolação
        for vertice in self.vertices.values():
            alvo = self.cor_padrao
            if self.vertice_hover is not None:
                if vertice.vertice_id == self.vertice_hover.vertice_id or self.esta_diretamente_conectado(self.vertice_hover, vertice):
                    alvo = self.cor_selecionado
                else:
                    alvo = self.cor_dessaturado
            vertice.cor_atual = interpolar_cor(vertice.cor_atual, alvo, self.fade_alpha) # Mudar cor de forma suave

            vertice.update()

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

        self.setWindowTitle("Grafla") # Nome da janela

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

    def comecar_aresta(self):
        if self.grafoWidget.vertice_selecionado:
            self.grafoWidget.comeco_aresta = self.grafoWidget.vertice_selecionado

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(1280, 720)  # Tamanho inicial da janela (Pode ser modificado pelo usuário)
    window.show()
    sys.exit(app.exec())